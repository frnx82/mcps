#!/usr/bin/env python3
"""Multi-Database MCP Server — powered by FastMCP.

Exposes Oracle, Impala, BigQuery, CloudSQL as MCP tools using the FastMCP
decorator-based API. All protocol handling (JSON-RPC, SSE, stdio) is managed
by the framework.

Supports two modes:
  - Production: Connects to real databases via environment variables
  - Mock: Generates realistic sample data for development/testing

Usage:
  python main.py              # Production mode (requires DB env vars)
  python main.py --mock       # Mock mode (no databases needed)
  fastmcp dev main.py         # Interactive dev/test UI
"""

import os
import sys
import json
import time
import logging
from typing import Optional

from fastmcp import FastMCP

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
MOCK_MODE_FLAG = True if "--mock" in sys.argv else MOCK_MODE


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
# FastMCP Server
# ══════════════════════════════════════════════════════════════════════════════

mcp = FastMCP(
    "database-mcp",
    description="Multi-Database MCP Server — Oracle, Impala, BigQuery, CloudSQL",
)


# ══════════════════════════════════════════════════════════════════════════════
# MCP Tools
# ══════════════════════════════════════════════════════════════════════════════

@mcp.tool()
def list_databases() -> str:
    """List all configured database connections (Oracle, Impala, BigQuery, CloudSQL)
    with their current status and health information."""
    databases = []
    for name, conn in _connectors.items():
        info = conn.get_info()
        health = conn.health_check()
        info["health"] = health
        databases.append(info)

    result = {
        "databases": databases,
        "total": len(databases),
        "mode": "mock" if MOCK_MODE_FLAG else "production",
        "read_only": READ_ONLY,
    }
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def list_schemas(database: str) -> str:
    """List all schemas (or datasets for BigQuery) in a specific database connection.

    Args:
        database: Database connection name (e.g., 'oracle', 'impala', 'bigquery', 'cloudsql')
    """
    conn = get_connector(database)
    schemas = conn.list_schemas()
    result = {
        "database": database,
        "schemas": schemas,
        "count": len(schemas),
    }
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def list_tables(database: str, schema: Optional[str] = None) -> str:
    """List all tables in a specific database and optional schema.
    Returns table names, types (TABLE/VIEW), and row counts when available.

    Args:
        database: Database connection name (e.g., 'oracle', 'impala', 'bigquery', 'cloudsql')
        schema: Schema or dataset name (optional — lists all if omitted)
    """
    conn = get_connector(database)
    tables = conn.list_tables(schema)
    result = {
        "database": database,
        "schema": schema,
        "tables": [t.to_dict() for t in tables],
        "count": len(tables),
    }
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def describe_table(database: str, table: str, schema: Optional[str] = None) -> str:
    """Get detailed column information for a table: column names, data types,
    nullability, primary keys, and defaults.

    Args:
        database: Database connection name
        table: Table name
        schema: Schema name (optional)
    """
    conn = get_connector(database)
    columns = conn.describe_table(table, schema)
    result = {
        "database": database,
        "schema": schema,
        "table": table,
        "columns": [c.to_dict() for c in columns],
        "column_count": len(columns),
    }
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def execute_query(database: str, sql: str, limit: int = DEFAULT_ROW_LIMIT) -> str:
    """Execute a SQL query against a specific database and return results.
    Supports Oracle, Impala, BigQuery, and CloudSQL SQL dialects.
    Results are limited to prevent memory issues.

    Args:
        database: Database connection name
        sql: SQL query to execute
        limit: Max rows to return (default: 100, max: 1000)
    """
    conn = get_connector(database)

    # Security validation
    sql = validate_query(sql, conn.db_type)
    sql = enforce_row_limit(sql, limit, conn.db_type)

    start = time.monotonic()
    result = conn.execute(sql)
    elapsed = (time.monotonic() - start) * 1000
    logger.info("  ✓ execute_query completed in %.1fms", elapsed)

    # Check if we hit the limit
    if result.row_count >= limit:
        result.truncated = True

    return json.dumps(result.to_dict(), indent=2, default=str)


@mcp.tool()
def get_sample_data(database: str, table: str, schema: Optional[str] = None, limit: int = 10) -> str:
    """Get sample rows from a table. Quick way to preview data
    without writing a SQL query.

    Args:
        database: Database connection name
        table: Table name
        schema: Schema name (optional)
        limit: Number of sample rows (default: 10, max: 50)
    """
    limit = min(limit, 50)
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
    return json.dumps(result.to_dict(), indent=2, default=str)


@mcp.tool()
def get_schema_context(database: str, schema: Optional[str] = None) -> str:
    """Get the full schema context (all tables and columns) for a database.
    Use this to understand the database structure before generating SQL queries.
    Ideal for natural language to SQL translation.

    Args:
        database: Database connection name
        schema: Specific schema to describe (optional — describes all if omitted)
    """
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

    result = {
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
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def health_check() -> str:
    """Check connectivity and health of all configured database connections."""
    results = {}
    for name, conn in _connectors.items():
        results[name] = conn.health_check()

    all_ok = all(r.get("status") == "ok" for r in results.values())
    result = {
        "overall_status": "ok" if all_ok else "degraded",
        "databases": results,
        "mode": "mock" if MOCK_MODE_FLAG else "production",
    }
    return json.dumps(result, indent=2, default=str)


# ══════════════════════════════════════════════════════════════════════════════
# MCP Resources
# ══════════════════════════════════════════════════════════════════════════════

@mcp.resource("server://info")
def server_info() -> str:
    """Server metadata and configuration."""
    return json.dumps({
        "name": "database-mcp",
        "version": "2.0.0",
        "description": "Multi-Database MCP Server (Oracle, Impala, BigQuery, CloudSQL)",
        "mode": "mock" if MOCK_MODE_FLAG else "production",
        "databases": list(_connectors.keys()),
        "read_only": READ_ONLY,
        "default_row_limit": DEFAULT_ROW_LIMIT,
        "max_row_limit": MAX_ROW_LIMIT,
    }, indent=2)


# ══════════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════════

def main():
    """Start the Multi-Database MCP Server."""
    banner = f"""
╔══════════════════════════════════════════════════════════════╗
║       Multi-Database MCP Server v2.0.0 (FastMCP)            ║
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

    # Run the FastMCP server
    mcp.run()


if __name__ == "__main__":
    main()
