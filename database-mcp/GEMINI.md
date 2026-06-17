# GEMINI.md — AI Agent Development Context

This file provides context and instructions for AI agents (Gemini, Claude, etc.)
working on the `database-mcp` project. It serves as a feedback loop to improve
agent interactions with this codebase over time.

---

## Project Summary

**Multi-Database MCP Server** — A unified MCP (Model Context Protocol) gateway
that connects AI agents to Oracle (on-prem), Impala (on-prem), BigQuery (GCP),
and CloudSQL (GCP) databases.

- **Language**: Python 3.9+
- **Protocol**: MCP JSON-RPC over HTTP (no FastMCP dependency)
- **Pattern**: Follows `mcp_splunk` structure from `mcps/services/`
- **Deployment Target**: Google Distributed Cloud (GDC)

---

## Architecture

```
main.py                  ← HTTP JSON-RPC server + MCP tool definitions
config.py                ← Environment-based configuration loader
security.py              ← SQL validation, injection protection, row limits
connectors/
  __init__.py            ← BaseConnector ABC + QueryResult/TableInfo/ColumnInfo dataclasses
  oracle_connector.py    ← oracledb (thin mode, connection pooling)
  impala_connector.py    ← impyla (HiveServer2, Kerberos/LDAP support)
  bigquery_connector.py  ← google-cloud-bigquery (SA/WI auth)
  cloudsql_connector.py  ← pg8000 (PostgreSQL) / PyMySQL (MySQL)
  mock_connector.py      ← Realistic mock data for testing
manifests/
  deploy.yaml            ← K8s Deployment + Service (GDC-compatible)
```

---

## Key Design Decisions

### Why HTTP JSON-RPC instead of FastMCP?
- Matches the existing `mcp_splunk` pattern in the monorepo
- Zero external dependencies for the core server
- Full control over request handling and error formatting
- Works with any HTTP client (not just MCP SDK clients)

### Why thin-mode oracledb?
- No Oracle Client installation needed in Docker
- Pure Python — simpler Docker images, no native libs
- Works on all platforms including ARM

### Why read-only by default?
- Safety first — agents shouldn't modify production data accidentally
- Can be toggled with `READ_ONLY=false` for specific use cases
- SQL validation catches write operations before they reach the database

### Why mock mode?
- Enables development without database access
- CI/CD testing without infrastructure
- Demo/POC scenarios
- Realistic financial data (trades, orders, positions)

---

## Coding Conventions

- **Python 3.9+ compatible** (deployed Python version on GDC)
- **Type hints** on all function signatures
- **Docstrings** on all classes and public methods
- **Logging** via `logging` module, not `print()`
- **Environment variables** for all configuration (12-factor app)
- **No global mutable state** except `_connectors` registry
- **Error messages** must never expose credentials (use `mask_credentials()`)

---

## Adding a New Database Connector

1. Create `connectors/newdb_connector.py`
2. Implement `BaseConnector` (see `connectors/__init__.py`)
3. Add config loading in `config.py` (new env vars)
4. Add factory case in `main.py::_create_connector()`
5. Add mock data in `connectors/mock_connector.py::MOCK_SCHEMAS`
6. Update `requirements.txt` with the driver
7. Update `manifests/deploy.yaml` with new Secret keys
8. Update docs

---

## Adding a New MCP Tool

1. Define the handler function in `main.py` (pattern: `tool_<name>(arguments)`)
2. Add to the `TOOLS` dict with:
   - `description` (shown to AI agents)
   - `inputSchema` (JSON Schema for parameters)
   - `handler` (the function)
3. The tool is automatically registered via `tools/list`

---

## Testing

### Mock Mode (no dependencies)
```bash
python3 main.py --mock
```

### Curl Test Template
```bash
curl -s -X POST http://localhost:8080 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "<TOOL_NAME>",
      "arguments": { <ARGS> }
    }
  }' | python3 -m json.tool
```

### Security Test
```bash
# This should be REJECTED (read-only mode)
curl -s -X POST http://localhost:8080 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"execute_query","arguments":{"database":"oracle","sql":"DROP TABLE users"}}}'
```

---

## Known Issues & TODOs

### Current Limitations
- [ ] No connection retry/reconnect logic yet
- [ ] No query result caching
- [ ] No SSE transport (HTTP only)
- [ ] Impala connector doesn't support parameterized queries (impyla limitation)
- [ ] BigQuery parameterized queries only support STRING, INT64, FLOAT64

### Planned Improvements
- [ ] Connection pool health monitoring and auto-reconnect
- [ ] Query result caching with configurable TTL
- [ ] SSE transport support for streaming results
- [ ] Query history/audit logging
- [ ] Rate limiting per client
- [ ] mTLS support for database connections
- [ ] Prometheus metrics endpoint (/metrics)
- [ ] Support for additional databases (Snowflake, Cassandra, MongoDB)

---

## Feedback Loop

When working on this project, please update this file with:
1. **New design decisions** and their rationale
2. **Bugs encountered** and their fixes
3. **Performance observations** from production
4. **Schema changes** or new connector patterns
5. **Security findings** or new injection patterns to block

This file is the single source of truth for AI agents working on this codebase.
Last updated: 2026-06-17
