# Multi-Database MCP Server

A Model Context Protocol (MCP) server that provides a unified interface to query multiple databases:
- **Oracle** (on-prem) via `oracledb` (thin mode)
- **Impala** (on-prem) via `impyla`
- **BigQuery** (GCP) via `google-cloud-bigquery`
- **CloudSQL** (GCP) via `pg8000` (PostgreSQL) / `PyMySQL` (MySQL)

Designed for deployment on **Google Distributed Cloud (GDC)** with non-root security context.

## Quick Start

### Mock Mode (no databases needed)

```bash
cd mcps/database-mcp
python main.py --mock
```

### Test with curl

```bash
# List available databases
curl -s -X POST http://localhost:8080 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"list_databases","arguments":{}}}' | python -m json.tool

# List tables in Oracle
curl -s -X POST http://localhost:8080 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"list_tables","arguments":{"database":"oracle","schema":"TRADING"}}}' | python -m json.tool

# Describe a table
curl -s -X POST http://localhost:8080 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"describe_table","arguments":{"database":"oracle","table":"TRADES","schema":"TRADING"}}}' | python -m json.tool

# Execute a query
curl -s -X POST http://localhost:8080 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"execute_query","arguments":{"database":"oracle","sql":"SELECT * FROM TRADES WHERE TRADE_STATUS = '\''SETTLED'\''"}}}' | python -m json.tool

# Get schema context (for NL→SQL)
curl -s -X POST http://localhost:8080 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"get_schema_context","arguments":{"database":"oracle","schema":"TRADING"}}}' | python -m json.tool

# Health check
curl -s http://localhost:8080/health | python -m json.tool
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
Agent (LLM)
    ↓ MCP JSON-RPC
database-mcp (this server)
    ├── Oracle Connector  →  Oracle DB (on-prem)
    ├── Impala Connector  →  Impala Cluster (on-prem)
    ├── BigQuery Connector → BigQuery (GCP)
    └── CloudSQL Connector → CloudSQL (GCP, via Auth Proxy)
```
