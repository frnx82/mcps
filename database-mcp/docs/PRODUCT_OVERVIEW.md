# Multi-Database MCP Server — Product Overview (FastMCP)

## What Is It?

The **Multi-Database MCP Server** is a unified data gateway that connects AI agents to multiple enterprise databases through the [Model Context Protocol (MCP)](https://modelcontextprotocol.io). Built with **FastMCP 3.x**, it enables AI-powered applications running on **Google Distributed Cloud (GDC)** to query, explore, and understand data across **Oracle**, **Impala**, **BigQuery**, and **CloudSQL** — all through a single, standardized interface.

Instead of building custom integrations for each database, your agents connect to one MCP server and access all your data through natural, tool-based interactions. FastMCP's decorator-based API provides automatic schema generation, multi-transport support (SSE, stdio, HTTP), and built-in developer tooling.

```
┌─────────────────────────────────────────────────────────┐
│          AI Agent (Claude, Cursor, Custom)                │
│         "Show me all settled trades from today"          │
└──────────────────────┬──────────────────────────────────┘
                       │ MCP (SSE / stdio / HTTP)
┌──────────────────────▼──────────────────────────────────┐
│         Multi-Database MCP Server (FastMCP 3.x)          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐ │
│  │  Oracle   │ │  Impala  │ │ BigQuery │ │  CloudSQL  │ │
│  │ (on-prem) │ │(on-prem) │ │  (GCP)   │ │   (GCP)    │ │
│  └──────────┘ └──────────┘ └──────────┘ └────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## Features

### 🔌 Multi-Database Connectivity
| Database | Location | Driver | Auth Support |
|----------|----------|--------|-------------|
| **Oracle** | On-Prem | `oracledb` (thin mode — no Oracle Client needed) | Username/Password, TNS, Easy Connect |
| **Impala** | On-Prem | `impyla` (HiveServer2) | NOSASL, LDAP, PLAIN, Kerberos (GSSAPI) |
| **BigQuery** | GCP | `google-cloud-bigquery` | Service Account, Workload Identity, ADC |
| **CloudSQL** | GCP | `pg8000` / `PyMySQL` | Username/Password via Cloud SQL Auth Proxy |

### 🔧 8 MCP Tools

| Tool | Purpose | Use Case |
|------|---------|----------|
| `list_databases` | Discover all connected databases | "What databases are available?" |
| `list_schemas` | Browse schemas/datasets | "What schemas does Oracle have?" |
| `list_tables` | Browse tables in a schema | "Show me all tables in the TRADING schema" |
| `describe_table` | Get column details (types, PKs, nullability) | "What columns does the TRADES table have?" |
| `execute_query` | Run SQL queries | "Run: SELECT * FROM TRADES WHERE status='SETTLED'" |
| `get_sample_data` | Preview table data | "Show me sample data from the POSITIONS table" |
| `get_schema_context` | Full schema metadata for NL→SQL | "Give me the full schema so I can write a query" |
| `health_check` | Monitor database connectivity | "Are all databases healthy?" |

### 🛡️ Enterprise Security

- **Read-Only Mode** (default): Blocks INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE
- **SQL Injection Protection**: Detects and blocks common injection patterns (UNION, EXEC, multi-statement, comment-based)
- **Row Limits**: Configurable max rows (default 100, hard limit 1000) to prevent memory exhaustion
- **Query Length Limits**: Blocks queries over 10K characters
- **Credential Masking**: Never exposes passwords in logs or error messages
- **Non-Root Container**: Runs as UID 1000 with dropped capabilities and seccomp profile

### 🧪 Mock Mode

Full mock mode with realistic financial data for development and testing:
- **4 simulated databases** with realistic schemas (TRADING, RISK, REFERENCE, etc.)
- **Sample trade data** with real-looking instrument IDs, counterparties, prices
- **No dependencies** — runs without any database drivers installed
- Start with: `python main.py --mock`
- Test interactively: `fastmcp dev main.py`

---

## Capabilities

### Data Discovery
An agent can explore your entire data landscape without prior knowledge:
```
Agent: "What databases do we have?"
→ Oracle (On-Prem), Impala (On-Prem), BigQuery (GCP), CloudSQL (GCP)

Agent: "What's in the Oracle database?"
→ Schemas: TRADING, RISK, REFERENCE, AUDIT

Agent: "Show me TRADING tables"
→ TRADES (1.5M rows), ORDERS (3.2M rows), POSITIONS (85K rows)

Agent: "Describe the TRADES table"
→ TRADE_ID (PK), TRADE_DATE, INSTRUMENT_ID, QUANTITY, PRICE, CURRENCY...
```

### Natural Language Querying (via Agent)
The `get_schema_context` tool provides full schema metadata to the AI agent, enabling it to generate accurate SQL from plain English:
```
User: "How many trades were settled yesterday?"
Agent: [calls get_schema_context → gets column info → generates SQL]
Agent: [calls execute_query with: SELECT COUNT(*) FROM TRADING.TRADES 
        WHERE TRADE_STATUS='SETTLED' AND TRADE_DATE=DATE'2026-06-16']
→ Result: 12,847 trades settled yesterday
```

### Cross-Database Analysis
Query different databases in sequence to combine insights:
```
User: "Compare Oracle trade volumes with BigQuery reporting totals"
Agent: [queries Oracle TRADES table → gets today's volume]
Agent: [queries BigQuery trade_summary → gets reported volume]
Agent: "Oracle shows 15,230 trades today. BigQuery reporting shows 15,228. 
        There's a discrepancy of 2 trades."
```

### Schema Understanding
Before writing queries, agents can understand the full data model:
- Column types and relationships
- Primary keys and constraints
- Table sizes (row counts)
- Database-specific SQL dialects

---

## Benefits

### 🚀 Accelerated Development
- **Single integration point** for all databases — no custom connectors per data source
- **Standard MCP protocol** — works with any MCP-compatible agent or client (Claude Desktop, Cursor, etc.)
- **Decorator-based tools** — add a new tool with `@mcp.tool()` and a typed function
- **Interactive testing** — `fastmcp dev` provides a browser-based test UI
- **Mock mode** for rapid development without database access

### 💰 Cost Efficiency
- **No per-query API costs** — direct database connections, not paid APIs
- **Connection pooling** (Oracle) — reuses connections efficiently
- **Row limits** prevent expensive full-table scans

### 🔒 Security First
- **Read-only by default** — agents can explore but can't modify data
- **No credential exposure** — all secrets via Kubernetes Secrets
- **SQL injection protection** — built-in validation layer

### 🏗️ Enterprise Ready
- **GDC-native** — designed for Google Distributed Cloud from day one
- **Non-root container** — complies with strict Pod Security Policies
- **Health endpoints** — Kubernetes readiness and liveness probes
- **Structured logging** — easy integration with observability stacks

### 🔄 Extensibility
- **Pluggable connector architecture** — add new databases by implementing `BaseConnector`
- **Tool-based design** — add new MCP tools with a simple `@mcp.tool()` decorator
- **Resource support** — expose server metadata via `@mcp.resource()`
- **Multi-transport** — SSE, stdio, and HTTP out of the box (no code changes)
- **Environment-driven config** — no code changes to add new connections

---

## Target Users

| Role | How They Use It |
|------|----------------|
| **Application Developers** | Connect apps running on GDC to query databases via MCP |
| **Data Engineers** | Build AI agents that explore and validate data pipelines |
| **Operations Teams** | Monitor database health and query operational data |
| **Risk/Compliance** | Run ad-hoc queries on transaction and reference data |
| **Business Analysts** | Ask questions in natural language and get data answers |

---

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.11 |
| Framework | **FastMCP 3.x** (PrefectHQ) |
| Protocol | MCP over SSE, stdio, HTTP |
| Transport | Auto-negotiated by FastMCP |
| Container | Python 3.11-slim, UID 1000 |
| Deployment | Kubernetes (GDC), Helm-compatible |
| Client Compat | Claude Desktop, Cursor, custom MCP clients |
| Observability | Structured logging, health_check tool |
