# Multi-Database MCP Server — Deployment & Usage Guide

## Table of Contents
- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [GDC Deployment](#gdc-deployment)
- [Connecting an Agent](#connecting-an-agent)
- [Tool Usage Reference](#tool-usage-reference)
- [Configuration Reference](#configuration-reference)
- [Troubleshooting](#troubleshooting)

---

## Local Development

### Prerequisites
- Python 3.9+
- No database drivers needed for mock mode

### Quick Start (Mock Mode)

```bash
cd mcps/database-mcp

# Run directly — no pip install needed for mock mode
python3 main.py --mock

# Or with custom port
PORT=9090 python3 main.py --mock
```

You should see:
```
╔══════════════════════════════════════════════════════════════╗
║       Multi-Database MCP Server v1.0.0                      ║
║       Oracle · Impala · BigQuery · CloudSQL                  ║
╠══════════════════════════════════════════════════════════════╣
║  Mode:       MOCK (no real connections)                      ║
║  Port:       8080                                            ║
║  Read-only:  True                                            ║
╚══════════════════════════════════════════════════════════════╝

🚀 MCP Server listening on http://0.0.0.0:8080
```

### Production Mode (Real Databases)

```bash
# Install database drivers
pip install -r requirements.txt

# Set connection environment variables
export ORACLE_HOST=oracle.internal.db
export ORACLE_SERVICE_NAME=TRADINGDB
export ORACLE_USER=app_reader
export ORACLE_PASSWORD=secret

export BIGQUERY_PROJECT=my-gcp-project
export BIGQUERY_CREDENTIALS_PATH=/path/to/service-account.json

# Start
python3 main.py
```

---

## Docker Deployment

### Build

```bash
cd mcps/database-mcp
docker build -t database-mcp:latest .
```

### Run (Mock Mode)

```bash
docker run -p 8080:8080 -e MOCK_MODE=true database-mcp:latest
```

### Run (Production)

```bash
docker run -p 8080:8080 \
  -e ORACLE_HOST=oracle.internal.db \
  -e ORACLE_SERVICE_NAME=TRADINGDB \
  -e ORACLE_USER=app_reader \
  -e ORACLE_PASSWORD=secret \
  -e BIGQUERY_PROJECT=my-project \
  -v /path/to/sa-key.json:/app/credentials.json:ro \
  -e BIGQUERY_CREDENTIALS_PATH=/app/credentials.json \
  -e IMPALA_HOST=impala.internal.db \
  -e CLOUDSQL_HOST=127.0.0.1 \
  -e CLOUDSQL_TYPE=postgres \
  -e CLOUDSQL_USER=appuser \
  -e CLOUDSQL_PASSWORD=secret \
  -e CLOUDSQL_DATABASE=appdb \
  database-mcp:latest
```

### Verify

```bash
# Health check
curl http://localhost:8080/health

# Server info
curl http://localhost:8080/
```

---

## GDC Deployment

### Step 1: Create Kubernetes Secrets

```bash
kubectl create secret generic database-mcp-secrets \
  --from-literal=oracle-host=oracle.internal.db \
  --from-literal=oracle-service-name=TRADINGDB \
  --from-literal=oracle-user=app_reader \
  --from-literal=oracle-password=<password> \
  --from-literal=impala-host=impala.internal.db \
  --from-literal=bigquery-project=my-gcp-project \
  --from-literal=cloudsql-user=appuser \
  --from-literal=cloudsql-password=<password> \
  --from-literal=cloudsql-database=appdb
```

### Step 2: Push Docker Image

```bash
# Tag for your GDC registry
docker tag database-mcp:latest gcr.io/<project>/database-mcp:latest

# Push
docker push gcr.io/<project>/database-mcp:latest
```

### Step 3: Update Image in deploy.yaml

Edit `manifests/deploy.yaml`:
```yaml
image: gcr.io/<project>/database-mcp:latest
```

### Step 4: Deploy

```bash
kubectl apply -f manifests/deploy.yaml
```

### Step 5: Verify

```bash
# Check pod status
kubectl get pods -l app=database-mcp

# Check logs
kubectl logs -l app=database-mcp -f

# Port-forward to test locally
kubectl port-forward svc/database-mcp 8080:8080

# Health check
curl http://localhost:8080/health
```

### CloudSQL Auth Proxy (if using CloudSQL)

Uncomment the Cloud SQL Auth Proxy sidecar in `deploy.yaml` and update the instance connection string:

```yaml
- name: cloud-sql-proxy
  image: gcr.io/cloud-sql-connectors/cloud-sql-proxy:2.8.0
  args:
    - "--port=5432"
    - "my-project:us-central1:my-instance"
```

---

## Connecting an Agent

### Architecture

```
┌──────────────────────────┐     ┌──────────────────────┐
│     Your AI Agent        │     │  database-mcp        │
│  (Python/Node.js/etc.)   │────▶│  (HTTP :8080)        │
│                          │     │                      │
│  1. User asks question   │     │  ┌────────────────┐  │
│  2. Agent calls MCP tool │     │  │ Oracle         │  │
│  3. MCP returns data     │     │  │ Impala         │  │
│  4. Agent formats answer │     │  │ BigQuery       │  │
│                          │     │  │ CloudSQL       │  │
└──────────────────────────┘     └──────────────────────┘
```

### Python Agent Example

```python
import json
import requests

MCP_URL = "http://database-mcp:8080"  # In-cluster URL
# or "http://localhost:8080" for local development


def call_mcp_tool(tool_name: str, arguments: dict) -> dict:
    """Call an MCP tool and return the parsed result."""
    response = requests.post(MCP_URL, json={
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments,
        },
    })
    result = response.json()

    if "error" in result:
        raise Exception(result["error"]["message"])

    # Parse the MCP text content
    text = result["result"]["content"][0]["text"]
    return json.loads(text)


# ── Example: Natural Language Query Flow ──────────────────

# Step 1: Get schema context
schema = call_mcp_tool("get_schema_context", {
    "database": "oracle",
    "schema": "TRADING"
})
print(f"Found {schema['table_count']} tables")

# Step 2: Send schema + user question to LLM to generate SQL
# (This is where your LLM/Gemini call goes)
user_question = "How many trades were settled yesterday?"
# llm_response = gemini.generate(prompt=f"Given schema: {schema}, write SQL for: {user_question}")
# generated_sql = llm_response.text

# Step 3: Execute the generated SQL
result = call_mcp_tool("execute_query", {
    "database": "oracle",
    "sql": "SELECT COUNT(*) as trade_count FROM TRADING.TRADES WHERE TRADE_STATUS='SETTLED' AND TRADE_DATE = TRUNC(SYSDATE-1)",
})
print(f"Result: {result['rows']}")

# Step 4: Format and return to user
# llm_response = gemini.generate(prompt=f"Format this result for the user: {result}")
```

### Using with Gemini API

```python
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-2.0-flash")


def ask_database(question: str, database: str = "oracle") -> str:
    """Ask a natural language question and get a data answer."""

    # 1. Get schema context
    schema = call_mcp_tool("get_schema_context", {"database": database})

    # 2. Generate SQL with Gemini
    sql_prompt = f"""You are a SQL expert. Given this database schema:
{json.dumps(schema['tables'], indent=2)}

Database type: {schema['db_type']}

Generate a SQL query to answer: "{question}"
Return ONLY the SQL query, nothing else."""

    sql_response = model.generate_content(sql_prompt)
    sql = sql_response.text.strip().strip("`").replace("sql\n", "")

    # 3. Execute the query
    result = call_mcp_tool("execute_query", {
        "database": database,
        "sql": sql,
    })

    # 4. Format the answer with Gemini
    answer_prompt = f"""The user asked: "{question}"

The SQL query returned:
Columns: {result['columns']}
Data: {result['rows']}
Row count: {result['row_count']}

Provide a clear, concise answer to the user's question based on this data."""

    answer = model.generate_content(answer_prompt)
    return answer.text


# Usage
print(ask_database("Show me today's top 5 trades by value"))
print(ask_database("What's the total trading volume in EUR?"))
print(ask_database("Which counterparty has the most pending trades?"))
```

### Connecting via Claude Desktop (MCP Client)

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "database-mcp": {
      "url": "http://localhost:8080",
      "transport": "http"
    }
  }
}
```

### Service Mesh / Internal DNS

In GDC, other pods access the MCP server via the Kubernetes Service:

```
http://database-mcp.default.svc.cluster.local:8080
```

Or simply:

```
http://database-mcp:8080
```

---

## Tool Usage Reference

### List Databases

```bash
curl -s -X POST http://localhost:8080 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "list_databases",
      "arguments": {}
    }
  }'
```

### List Tables

```bash
curl -s -X POST http://localhost:8080 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
      "name": "list_tables",
      "arguments": {
        "database": "oracle",
        "schema": "TRADING"
      }
    }
  }'
```

### Execute Query

```bash
curl -s -X POST http://localhost:8080 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
      "name": "execute_query",
      "arguments": {
        "database": "oracle",
        "sql": "SELECT * FROM TRADING.TRADES WHERE TRADE_STATUS = '\''SETTLED'\'' AND TRADE_DATE >= DATE '\''2026-06-01'\''",
        "limit": 50
      }
    }
  }'
```

### Get Schema Context (for NL→SQL)

```bash
curl -s -X POST http://localhost:8080 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 4,
    "method": "tools/call",
    "params": {
      "name": "get_schema_context",
      "arguments": {
        "database": "oracle",
        "schema": "TRADING"
      }
    }
  }'
```

---

## Configuration Reference

See [README.md](../README.md#environment-variables) for the complete list of environment variables.

### Key Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8080` | Server listening port |
| `MOCK_MODE` | `false` | Enable mock data mode |
| `READ_ONLY` | `true` | Block write operations |
| `DEFAULT_ROW_LIMIT` | `100` | Default max rows returned |
| `MAX_ROW_LIMIT` | `1000` | Absolute maximum rows |
| `QUERY_TIMEOUT_SECONDS` | `30` | Query timeout |
| `LOG_LEVEL` | `INFO` | Logging verbosity |

---

## Troubleshooting

### Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| `Address already in use` | Port 8080 taken | Use `PORT=8090 python3 main.py --mock` |
| `No database connections configured` | Missing env vars | Set `ORACLE_HOST`, `BIGQUERY_PROJECT`, etc. |
| `Write operation not allowed` | Read-only mode (default) | Set `READ_ONLY=false` if writes are needed |
| `Query too long` | SQL > 10K chars | Simplify your query |
| `Database 'x' not found` | Env vars not set for that DB | Check env vars for that database |

### Health Check

```bash
# Quick health check
curl http://localhost:8080/health

# Detailed server info
curl http://localhost:8080/
```

### Logs

```bash
# Local
LOG_LEVEL=DEBUG python3 main.py --mock

# Kubernetes
kubectl logs -l app=database-mcp -f --tail=100
```
