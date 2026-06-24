# Multi-Database MCP Server (FastMCP)

A Model Context Protocol (MCP) server that provides a unified interface to query multiple databases:
- **Oracle** (on-prem) via `oracledb` (thin mode)
- **Impala** (on-prem) via `impyla`
- **BigQuery** (GCP) via `google-cloud-bigquery`
- **CloudSQL** (GCP) via `pg8000` (PostgreSQL) / `PyMySQL` (MySQL)

Built with **FastMCP 3.x** for automatic protocol handling, SSE/stdio transport, and decorator-based tool definitions.
Designed for deployment on **Google Distributed Cloud (GDC)** with non-root security context.

## Quick Start

### Install

```bash
cd mcps/database-mcp
pip install -r requirements.txt
```

### Mock Mode (no databases needed)

```bash
python main.py --mock
```

### Interactive Dev/Test UI

```bash
fastmcp dev main.py
```

### Connect from Claude Desktop / Cursor

Add to your MCP client config:

```json
{
  "mcpServers": {
    "database-mcp": {
      "command": "python",
      "args": ["main.py", "--mock"]
    }
  }
}
```

## MCP Tools

| Tool | Description |
|------|-------------|
| `list_databases` | List all configured connections with health status |
| `list_schemas` | List schemas/datasets in a database |
| `list_tables` | List tables in a database/schema |
| `describe_table` | Get column details (names, types, PKs) |
| `execute_query` | Run a SQL query (read-only by default) |
| `get_sample_data` | Preview rows from a table |
| `get_schema_context` | Full schema metadata for NL→SQL |
| `health_check` | Check all database connections |

## Environment Variables

### Server
| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8080` | Server port |
| `MOCK_MODE` | `false` | Enable mock mode |
| `READ_ONLY` | `true` | Block write queries |
| `DEFAULT_ROW_LIMIT` | `100` | Default max rows |
| `MAX_ROW_LIMIT` | `1000` | Absolute max rows |
| `LOG_LEVEL` | `INFO` | Logging level |

### Oracle
| Variable | Description |
|----------|-------------|
| `ORACLE_HOST` | Oracle host |
| `ORACLE_PORT` | Port (default: 1521) |
| `ORACLE_SERVICE_NAME` | Oracle service name |
| `ORACLE_DSN` | Full DSN (alternative to host/port/service) |
| `ORACLE_USER` | Username |
| `ORACLE_PASSWORD` | Password |

### Impala
| Variable | Description |
|----------|-------------|
| `IMPALA_HOST` | Impala host |
| `IMPALA_PORT` | Port (default: 21050) |
| `IMPALA_AUTH_MECHANISM` | NOSASL, PLAIN, LDAP, GSSAPI |
| `IMPALA_USER` | Username (for PLAIN/LDAP) |
| `IMPALA_PASSWORD` | Password (for PLAIN/LDAP) |
| `IMPALA_DATABASE` | Default database |

### BigQuery
| Variable | Description |
|----------|-------------|
| `BIGQUERY_PROJECT` | GCP project ID |
| `BIGQUERY_CREDENTIALS_PATH` | Service account JSON path |
| `BIGQUERY_LOCATION` | Dataset location (default: US) |
| `BIGQUERY_DATASET` | Default dataset |

### CloudSQL
| Variable | Description |
|----------|-------------|
| `CLOUDSQL_HOST` | Host (default: 127.0.0.1 for proxy) |
| `CLOUDSQL_PORT` | Port (5432 for PG, 3306 for MySQL) |
| `CLOUDSQL_TYPE` | `postgres` or `mysql` |
| `CLOUDSQL_USER` | Username |
| `CLOUDSQL_PASSWORD` | Password |
| `CLOUDSQL_DATABASE` | Database name |

## Docker

```bash
# Build
docker build -t database-mcp .

# Run (mock mode)
docker run -p 8080:8080 -e MOCK_MODE=true database-mcp

# Run (production)
docker run -p 8080:8080 \
  -e ORACLE_HOST=oracle.internal \
  -e ORACLE_USER=app \
  -e ORACLE_PASSWORD=secret \
  -e BIGQUERY_PROJECT=my-project \
  database-mcp
```

## Architecture

```
Agent (Claude, Cursor, custom)
    ↓ MCP (SSE / stdio / HTTP)
database-mcp (FastMCP 3.x)
    ├── Oracle Connector  →  Oracle DB (on-prem)
    ├── Impala Connector  →  Impala Cluster (on-prem)
    ├── BigQuery Connector → BigQuery (GCP)
    └── CloudSQL Connector → CloudSQL (GCP, via Auth Proxy)
```
