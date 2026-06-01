# Splunk MCP Server

A **Model Context Protocol (MCP) server** that wraps Splunk's search API, enabling any MCP-aware client to query Splunk logs via standard JSON-RPC over HTTP.

## Features

| Tool | Description |
|------|-------------|
| `splunk_search` | Run arbitrary SPL queries |
| `splunk_get_pod_logs` | Fetch pod/service logs with optional pattern/keyword filter |
| `splunk_search_by_correlation_id` | Trace a request across services by correlation/trace ID |
| `splunk_get_error_summary` | Error rate and breakdown for a service or index |
| `splunk_list_indexes` | List available Splunk indexes |
| `splunk_get_saved_searches` | List saved search reports |
| `splunk_health` | Check Splunk connection status |

## Quick Start

### Mock Mode (No Splunk Required)

```bash
cd services/mcp_splunk
pip install -r requirements.txt
python main.py --mock
# → MCP server running at http://localhost:8080
```

Mock mode provides realistic K8s pod logs with correlation IDs, errors, and stack traces.

### Production Mode

```bash
# Set Splunk credentials
export SPLUNK_INSTANCE=splunk.your-company.com
export SPLUNK_PORT=8089
export SPLUNK_SCHEME=https
export SPLUNK_TOKEN=<your-splunk-token>

# Start
python main.py
```

## Testing

```bash
# List available tools
curl -s -X POST http://localhost:8080 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":"1","method":"tools/list","params":{}}' | python -m json.tool

# Search pod logs
curl -s -X POST http://localhost:8080 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":"2","method":"tools/call","params":{"name":"splunk_get_pod_logs","arguments":{"service":"billing-service","pattern":"error","limit":10}}}' | python -m json.tool

# Trace by correlation ID
curl -s -X POST http://localhost:8080 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":"3","method":"tools/call","params":{"name":"splunk_search_by_correlation_id","arguments":{"correlation_id":"abc-123-def"}}}' | python -m json.tool
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SPLUNK_INSTANCE` | Prod | — | Splunk server hostname |
| `SPLUNK_PORT` | No | `8089` | Splunk management port |
| `SPLUNK_SCHEME` | No | `https` | `http` or `https` |
| `SPLUNK_TOKEN` | Prod | — | Splunk auth token |
| `SPLUNK_USERNAME` | Alt | — | Splunk username (if not using token) |
| `SPLUNK_PASSWORD` | Alt | — | Splunk password (if not using token) |
| `SPLUNK_INDEX` | No | `main` | Default Splunk index |
| `PORT` | No | `8080` | MCP server listen port |
| `MOCK_MODE` | No | `false` | Enable mock mode without `--mock` flag |

## Integration with GDC Dashboard

In `mock-project-gemini`, set:
```bash
export SPLUNK_MCP_URL=http://splunk-mcp-service:8080
```

Then call tools via JSON-RPC POST — same pattern as Jira MCP.
