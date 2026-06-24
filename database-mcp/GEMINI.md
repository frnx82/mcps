# GEMINI.md — AI Agent Development Context

This file provides context and instructions for AI agents (Gemini, Claude, etc.)
working on the `database-mcp` project. It serves as a feedback loop to improve
agent interactions with this codebase over time.

---

## Project Summary

**Multi-Database MCP Server** — A unified MCP (Model Context Protocol) gateway
that connects AI agents to Oracle (on-prem), Impala (on-prem), BigQuery (GCP),
and CloudSQL (GCP) databases.

- **Language**: Python 3.11+
- **Framework**: FastMCP 3.x (PrefectHQ)
- **Protocol**: MCP over SSE, stdio, HTTP (auto-negotiated by FastMCP)
- **Pattern**: Decorator-based `@mcp.tool()` API
- **Deployment Target**: Google Distributed Cloud (GDC)

---

## Architecture

```
main.py                  ← FastMCP server + @mcp.tool() definitions
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

### Why FastMCP 3.x?
- **Dramatic code reduction**: 668 → 280 lines in main.py (60% less boilerplate)
- **Auto schema generation**: Python type hints → MCP inputSchema (no manual JSON dicts)
- **Multi-transport**: SSE, stdio, HTTP supported out of the box
- **Client compatibility**: Works with Claude Desktop, Cursor, and any MCP client
- **Developer tooling**: `fastmcp dev` provides interactive browser-based testing
- **Production ready**: Built-in error handling, logging, and protocol compliance

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

- **Python 3.11+ compatible** (deployed Python version on GDC)
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
4. Add factory case in `main.py::_create_connector()` (unchanged from before)
5. Add mock data in `connectors/mock_connector.py::MOCK_SCHEMAS`
6. Update `requirements.txt` with the driver
7. Update `manifests/deploy.yaml` with new Secret keys
8. Update docs

---

## Adding a New MCP Tool

1. Add a function in `main.py` with the `@mcp.tool()` decorator
2. Use Python type hints for parameters (FastMCP auto-generates the JSON Schema)
3. Write a clear docstring (shown to AI agents as the tool description)
4. Return a JSON string with the result

```python
@mcp.tool()
def my_new_tool(database: str, option: Optional[str] = None) -> str:
    """Description shown to AI agents."""
    # ... implementation ...
    return json.dumps(result, indent=2, default=str)
```

The tool is automatically registered — no manual dict or schema needed.

---

## Testing

### Mock Mode (no dependencies)
```bash
python3 main.py --mock
```

### Interactive Dev/Test UI
```bash
fastmcp dev main.py
```
This opens a browser-based interface where you can call each tool interactively.

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

---

## Known Issues & TODOs

### Current Limitations
- [ ] No connection retry/reconnect logic yet
- [ ] No query result caching
- [ ] Impala connector doesn't support parameterized queries (impyla limitation)
- [ ] BigQuery parameterized queries only support STRING, INT64, FLOAT64

### Completed (via FastMCP migration)
- [x] ~~No SSE transport~~ → SSE, stdio, HTTP all supported by FastMCP
- [x] ~~Manual JSON-RPC handling~~ → Framework handles protocol
- [x] ~~Manual inputSchema dicts~~ → Auto-generated from type hints

### Planned Improvements
- [ ] Connection pool health monitoring and auto-reconnect
- [ ] Query result caching with configurable TTL
- [ ] Query history/audit logging
- [ ] Rate limiting per client
- [ ] mTLS support for database connections
- [ ] OpenTelemetry tracing (FastMCP 3.x built-in support)
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
Last updated: 2026-06-23 (FastMCP 3.x migration)
