#!/usr/bin/env python3
"""Multi-Database MCP Server — Exposes Oracle, Impala, BigQuery, CloudSQL as MCP tools.

Implements the MCP (Model Context Protocol) JSON-RPC interface using Python's
built-in http.server module (same pattern as mcp_splunk — no fastmcp dependency).

Supports two modes:
  - Production: Connects to real databases via environment variables
  - Mock: Generates realistic sample data for development/testing

Usage:
  python main.py          # Production mode (requires DB env vars)
  python main.py --mock   # Mock mode (no databases needed)
"""

import os
import sys
import json
import time
import logging
import traceback
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Any, Optional

# ── Logging setup ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("mcp_database")

# ── Import config ─────────────────────────────────────────────────────────────
from config import (
    MCP_PORT, MOCK_MODE, READ_ONLY, DEFAULT_ROW_LIMIT, MAX_ROW_LIMIT,
    QUERY_TIMEOUT_SECONDS, load_database_configs,
)
from security import validate_query, enforce_row_limit, QueryValidationError, mask_credentials
from connectors import QueryResult, TableInfo, ColumnInfo, BaseConnector

# Check CLI flags
if "--mock" in sys.argv:
    MOCK_MODE_FLAG = True
else:
    MOCK_MODE_FLAG = MOCK_MODE

# ══════════════════════════════════════════════════════════════════════════════
# Connector Registry
# ══════════════════════════════════════════════════════════════════════════════

_connectors: dict[str, BaseConnector] = {}


def initialize_connectors():
    """Initialize all configured database connectors."""
    global _connectors

    if MOCK_MODE_FLAG:
        logger.info("🔧 Starting in MOCK MODE — no real database connections")
        from connectors.mock_connector import MockConnector

        for db_name in ["oracle", "impala", "bigquery", "cloudsql"]:
            mock = MockConnector(db_name)
            mock.connect()
            _connectors[db_name] = mock
            logger.info("  ✓ Mock connector: %s", db_name)

    else:
        logger.info("🔌 Starting in PRODUCTION MODE — connecting to databases")
        configs = load_database_configs()

        if not configs:
            logger.warning("No database connections configured! Set env vars or use --mock")

        for name, cfg in configs.items():
            try:
                connector = _create_connector(name, cfg)
                connector.connect()
                _connectors[name] = connector
                logger.info("  ✓ Connected: %s (%s)", name, cfg.db_type)
            except Exception as e:
                logger.error("  ✗ Failed to connect '%s': %s", name, mask_credentials(str(e)))

    logger.info("Initialized %d database connector(s)", len(_connectors))


def _create_connector(name: str, cfg) -> BaseConnector:
    """Factory: create the appropriate connector based on db_type."""
    if cfg.db_type == "oracle":
        from connectors.oracle_connector import OracleConnector
        return OracleConnector(name, cfg.params)
    elif cfg.db_type == "impala":
        from connectors.impala_connector import ImpalaConnector
        return ImpalaConnector(name, cfg.params)
    elif cfg.db_type == "bigquery":
        from connectors.bigquery_connector import BigQueryConnector
        return BigQueryConnector(name, cfg.params)
    elif cfg.db_type in ("cloudsql_pg", "cloudsql_mysql"):
        from connectors.cloudsql_connector import CloudSQLConnector
        return CloudSQLConnector(name, cfg.db_type, cfg.params)
    else:
        raise ValueError(f"Unknown database type: {cfg.db_type}")


def get_connector(database: str) -> BaseConnector:
    """Get a connector by database name."""
    if database not in _connectors:
        available = ", ".join(_connectors.keys()) if _connectors else "(none)"
        raise ValueError(
            f"Database '{database}' not found. Available: {available}"
        )
    return _connectors[database]


# ══════════════════════════════════════════════════════════════════════════════
# MCP Tool Implementations
# ══════════════════════════════════════════════════════════════════════════════

def tool_list_databases(arguments: dict) -> dict:
    """List all configured database connections and their status."""
    databases = []
    for name, conn in _connectors.items():
        info = conn.get_info()
        health = conn.health_check()
        info["health"] = health
        databases.append(info)

    return {
        "databases": databases,
        "total": len(databases),
        "mode": "mock" if MOCK_MODE_FLAG else "production",
        "read_only": READ_ONLY,
    }


def tool_list_schemas(arguments: dict) -> dict:
    """List schemas/databases in a specific connection."""
    database = arguments.get("database", "")
    if not database:
        return {"error": "Parameter 'database' is required"}

    conn = get_connector(database)
    schemas = conn.list_schemas()
    return {
        "database": database,
        "schemas": schemas,
        "count": len(schemas),
    }


def tool_list_tables(arguments: dict) -> dict:
    """List tables in a specific database/schema."""
    database = arguments.get("database", "")
    schema = arguments.get("schema", None)

    if not database:
        return {"error": "Parameter 'database' is required"}

    conn = get_connector(database)
    tables = conn.list_tables(schema)
    return {
        "database": database,
        "schema": schema,
        "tables": [t.to_dict() for t in tables],
        "count": len(tables),
    }


def tool_describe_table(arguments: dict) -> dict:
    """Get column details for a table."""
    database = arguments.get("database", "")
    table = arguments.get("table", "")
    schema = arguments.get("schema", None)

    if not database:
        return {"error": "Parameter 'database' is required"}
    if not table:
        return {"error": "Parameter 'table' is required"}

    conn = get_connector(database)
    columns = conn.describe_table(table, schema)
    return {
        "database": database,
        "schema": schema,
        "table": table,
        "columns": [c.to_dict() for c in columns],
        "column_count": len(columns),
    }


def tool_execute_query(arguments: dict) -> dict:
    """Execute a SQL query against a specific database."""
    database = arguments.get("database", "")
    sql = arguments.get("sql", "")
    limit = arguments.get("limit", DEFAULT_ROW_LIMIT)

    if not database:
        return {"error": "Parameter 'database' is required"}
    if not sql:
        return {"error": "Parameter 'sql' is required"}

    conn = get_connector(database)

    # Security validation
    sql = validate_query(sql, conn.db_type)
    sql = enforce_row_limit(sql, limit, conn.db_type)

    result = conn.execute(sql)

    # Check if we hit the limit
    if result.row_count >= limit:
        result.truncated = True

    return result.to_dict()


def tool_get_sample_data(arguments: dict) -> dict:
    """Get sample rows from a table."""
    database = arguments.get("database", "")
    table = arguments.get("table", "")
    schema = arguments.get("schema", None)
    limit = min(arguments.get("limit", 10), 50)

    if not database:
        return {"error": "Parameter 'database' is required"}
    if not table:
        return {"error": "Parameter 'table' is required"}

    conn = get_connector(database)

    # Build safe SELECT
    if conn.db_type == "bigquery" and schema:
        qualified = f"`{schema}`.`{table}`"
    elif schema:
        qualified = f"{schema}.{table}"
    else:
        qualified = table

    sql = f"SELECT * FROM {qualified}"
    sql = enforce_row_limit(sql, limit, conn.db_type)

    result = conn.execute(sql)
    return result.to_dict()


def tool_get_schema_context(arguments: dict) -> dict:
    """Get full schema context for a database — useful for NL→SQL.

    Returns all tables and their columns to help an AI agent
    generate accurate SQL queries from natural language.
    """
    database = arguments.get("database", "")
    schema = arguments.get("schema", None)

    if not database:
        return {"error": "Parameter 'database' is required"}

    conn = get_connector(database)
    tables = conn.list_tables(schema)

    schema_context = []
    for t in tables[:50]:  # Limit to 50 tables to avoid token overflow
        try:
            columns = conn.describe_table(t.name, t.schema)
            schema_context.append({
                "table": t.name,
                "schema": t.schema,
                "type": t.table_type,
                "row_count": t.row_count,
                "columns": [c.to_dict() for c in columns],
            })
        except Exception:
            schema_context.append({
                "table": t.name,
                "schema": t.schema,
                "type": t.table_type,
                "columns": [],
                "error": "Could not retrieve column details",
            })

    return {
        "database": database,
        "db_type": conn.db_type,
        "tables": schema_context,
        "table_count": len(schema_context),
        "hint": (
            "Use this schema context to generate SQL queries. "
            "Always qualify table names with schema. "
            f"This database uses {conn.db_type} SQL dialect."
        ),
    }


def tool_health_check(arguments: dict) -> dict:
    """Check connectivity to all configured databases."""
    results = {}
    for name, conn in _connectors.items():
        results[name] = conn.health_check()

    all_ok = all(r.get("status") == "ok" for r in results.values())
    return {
        "overall_status": "ok" if all_ok else "degraded",
        "databases": results,
        "mode": "mock" if MOCK_MODE_FLAG else "production",
    }


# ══════════════════════════════════════════════════════════════════════════════
# MCP Tool Registry
# ══════════════════════════════════════════════════════════════════════════════

TOOLS = {
    "list_databases": {
        "description": (
            "List all configured database connections (Oracle, Impala, BigQuery, CloudSQL) "
            "with their current status and health information."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
        "handler": tool_list_databases,
    },
    "list_schemas": {
        "description": (
            "List all schemas (or datasets for BigQuery) in a specific database connection."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "database": {
                    "type": "string",
                    "description": "Database connection name (e.g., 'oracle', 'impala', 'bigquery', 'cloudsql')",
                },
            },
            "required": ["database"],
        },
        "handler": tool_list_schemas,
    },
    "list_tables": {
        "description": (
            "List all tables in a specific database and optional schema. "
            "Returns table names, types (TABLE/VIEW), and row counts when available."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "database": {
                    "type": "string",
                    "description": "Database connection name (e.g., 'oracle', 'impala', 'bigquery', 'cloudsql')",
                },
                "schema": {
                    "type": "string",
                    "description": "Schema or dataset name (optional — lists all if omitted)",
                },
            },
            "required": ["database"],
        },
        "handler": tool_list_tables,
    },
    "describe_table": {
        "description": (
            "Get detailed column information for a table: column names, data types, "
            "nullability, primary keys, and defaults."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "database": {
                    "type": "string",
                    "description": "Database connection name",
                },
                "table": {
                    "type": "string",
                    "description": "Table name",
                },
                "schema": {
                    "type": "string",
                    "description": "Schema name (optional)",
                },
            },
            "required": ["database", "table"],
        },
        "handler": tool_describe_table,
    },
    "execute_query": {
        "description": (
            "Execute a SQL query against a specific database and return results. "
            "Supports Oracle, Impala, BigQuery, and CloudSQL SQL dialects. "
            "Results are limited to prevent memory issues. "
            f"{'Read-only mode: only SELECT queries allowed.' if READ_ONLY else 'Read-write mode enabled.'}"
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "database": {
                    "type": "string",
                    "description": "Database connection name",
                },
                "sql": {
                    "type": "string",
                    "description": "SQL query to execute",
                },
                "limit": {
                    "type": "integer",
                    "description": f"Max rows to return (default: {DEFAULT_ROW_LIMIT}, max: {MAX_ROW_LIMIT})",
                },
            },
            "required": ["database", "sql"],
        },
        "handler": tool_execute_query,
    },
    "get_sample_data": {
        "description": (
            "Get sample rows from a table. Quick way to preview data "
            "without writing a SQL query."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "database": {
                    "type": "string",
                    "description": "Database connection name",
                },
                "table": {
                    "type": "string",
                    "description": "Table name",
                },
                "schema": {
                    "type": "string",
                    "description": "Schema name (optional)",
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of sample rows (default: 10, max: 50)",
                },
            },
            "required": ["database", "table"],
        },
        "handler": tool_get_sample_data,
    },
    "get_schema_context": {
        "description": (
            "Get the full schema context (all tables and columns) for a database. "
            "Use this to understand the database structure before generating SQL queries. "
            "Ideal for natural language to SQL translation."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "database": {
                    "type": "string",
                    "description": "Database connection name",
                },
                "schema": {
                    "type": "string",
                    "description": "Specific schema to describe (optional — describes all if omitted)",
                },
            },
            "required": ["database"],
        },
        "handler": tool_get_schema_context,
    },
    "health_check": {
        "description": "Check connectivity and health of all configured database connections.",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
        "handler": tool_health_check,
    },
}


# ══════════════════════════════════════════════════════════════════════════════
# MCP JSON-RPC Handler
# ══════════════════════════════════════════════════════════════════════════════

class MCPHandler(BaseHTTPRequestHandler):
    """HTTP JSON-RPC handler implementing the MCP protocol."""

    def log_message(self, format, *args):
        logger.debug(format, *args)

    def _send_json(self, data: dict, status: int = 200):
        body = json.dumps(data, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path == "/health":
            result = tool_health_check({})
            status = 200 if result["overall_status"] == "ok" else 503
            self._send_json(result, status)
        elif self.path == "/":
            self._send_json({
                "name": "database-mcp",
                "version": "1.0.0",
                "description": "Multi-Database MCP Server (Oracle, Impala, BigQuery, CloudSQL)",
                "mode": "mock" if MOCK_MODE_FLAG else "production",
                "databases": list(_connectors.keys()),
                "tools": list(TOOLS.keys()),
            })
        else:
            self._send_json({"error": "Not found"}, 404)

    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            request = json.loads(body)
        except (json.JSONDecodeError, ValueError) as e:
            self._send_json({
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {e}"},
            }, 400)
            return

        req_id = request.get("id")
        method = request.get("method", "")
        params = request.get("params", {})

        logger.info("→ %s (id=%s)", method, req_id)

        try:
            result = self._handle_method(method, params)
            self._send_json({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": result,
            })
        except QueryValidationError as e:
            self._send_json({
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32602, "message": str(e)},
            })
        except ValueError as e:
            self._send_json({
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32602, "message": str(e)},
            })
        except Exception as e:
            logger.error("Error handling %s: %s\n%s", method, e, traceback.format_exc())
            self._send_json({
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32603,
                    "message": mask_credentials(str(e)),
                },
            })

    def _handle_method(self, method: str, params: dict) -> Any:
        """Route MCP methods to handlers."""

        # ── MCP Protocol Methods ──────────────────────────────────────────
        if method == "initialize":
            return {
                "protocolVersion": "2024-11-05",
                "serverInfo": {
                    "name": "database-mcp",
                    "version": "1.0.0",
                },
                "capabilities": {
                    "tools": {"listChanged": False},
                },
            }

        elif method == "notifications/initialized":
            return {}

        elif method == "tools/list":
            tool_list = []
            for name, tool in TOOLS.items():
                tool_list.append({
                    "name": name,
                    "description": tool["description"],
                    "inputSchema": tool["inputSchema"],
                })
            return {"tools": tool_list}

        elif method == "tools/call":
            tool_name = params.get("name", "")
            arguments = params.get("arguments", {})

            if tool_name not in TOOLS:
                raise ValueError(f"Unknown tool: {tool_name}. Available: {', '.join(TOOLS.keys())}")

            logger.info("  🔧 Tool call: %s(%s)", tool_name, json.dumps(arguments, default=str)[:200])
            start = time.monotonic()
            result = TOOLS[tool_name]["handler"](arguments)
            elapsed = (time.monotonic() - start) * 1000
            logger.info("  ✓ %s completed in %.1fms", tool_name, elapsed)

            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(result, indent=2, default=str),
                    }
                ],
            }

        elif method == "ping":
            return {}

        else:
            raise ValueError(f"Unknown method: {method}")


# ══════════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════════

def main():
    """Start the Multi-Database MCP Server."""
    banner = f"""
╔══════════════════════════════════════════════════════════════╗
║       Multi-Database MCP Server v1.0.0                      ║
║       Oracle · Impala · BigQuery · CloudSQL                  ║
╠══════════════════════════════════════════════════════════════╣
║  Mode:       {'MOCK (no real connections)' if MOCK_MODE_FLAG else 'PRODUCTION':40s} ║
║  Port:       {MCP_PORT:<40d} ║
║  Read-only:  {str(READ_ONLY):<40s} ║
║  Row limit:  {f'{DEFAULT_ROW_LIMIT} (max {MAX_ROW_LIMIT})':<40s} ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)

    # Initialize database connectors
    initialize_connectors()

    # Start HTTP server
    server = HTTPServer(("0.0.0.0", MCP_PORT), MCPHandler)
    logger.info("🚀 MCP Server listening on http://0.0.0.0:%d", MCP_PORT)
    logger.info("   Health check: http://localhost:%d/health", MCP_PORT)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        # Disconnect all connectors
        for name, conn in _connectors.items():
            try:
                conn.disconnect()
            except Exception:
                pass
        server.server_close()
        logger.info("Server stopped.")


if __name__ == "__main__":
    main()
