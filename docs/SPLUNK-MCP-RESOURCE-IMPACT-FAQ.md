# Splunk MCP Server — Resource Impact & Service Account Justification

## Purpose of This Document

This document answers common questions from the **Splunk Platform Team** regarding our request for
a Splunk service account and API token. It provides a comprehensive resource impact assessment,
security posture, and operational safeguards built into our Splunk MCP integration.

---

## Executive Summary

We are building an **AI-powered SRE dashboard** (GDC Dashboard) that allows developers to ask
natural language questions about application logs. The AI agent calls a lightweight **MCP (Model
Context Protocol) server** that translates these questions into Splunk SPL queries via the
**Splunk Python SDK (`splunklib`)**.

**Key facts:**
- Equivalent to **one additional user** running searches in Splunk Web
- All queries have **hard-coded result caps** (50–100 results max)
- Default time ranges are **-1h to -24h** (never full-index scans)
- The AI agent is **rate-limited to 5 tool calls per chat turn**
- Queries use **normal search mode** (not real-time)
- The service account needs **read-only** access

---

## Frequently Asked Questions

### 1. What is this integration and how does it work?

Our GDC Dashboard has an AI chat feature powered by Google Gemini. When a developer asks a question
like *"show me errors from billing-service in the last hour"*, the AI agent:

1. Translates the natural language into a structured tool call (e.g., `splunk_get_pod_logs`)
2. The tool call is sent to our **Splunk MCP Server** (a lightweight Python service running in our GDC cluster)
3. The MCP server constructs an SPL query and executes it via the **Splunk Python SDK** (`splunklib.client.connect`)
4. Results are returned to the AI, which summarizes them in natural language for the developer

**The MCP server acts as a controlled proxy — developers never write SPL directly.**

```
Developer → AI Chat → Splunk MCP Server → Splunk REST API (port 8089) → Results
```

### 2. What Splunk queries will this generate?

The MCP server exposes **7 pre-defined tools**. Each generates predictable, bounded SPL:

| Tool | SPL Pattern Generated | Time Range | Max Results |
|------|----------------------|------------|-------------|
| `splunk_search` | User-defined SPL (passed through) | Default: `-1h` | 100 |
| `splunk_get_pod_logs` | `search index=<idx> service=<svc> [level=<lvl>] [pattern]` | Default: `-1h` | 50 |
| `splunk_search_by_correlation_id` | `search index=<idx> correlation_id=<id>` | Default: `-24h` | 100 |
| `splunk_get_error_summary` | `search index=<idx> level=ERROR \| stats count by service` | Default: `-24h` | 100 |
| `splunk_list_indexes` | REST API call (`/services/data/indexes`) | N/A | N/A |
| `splunk_get_saved_searches` | REST API call (`/services/saved/searches`) | N/A | N/A |
| `splunk_health` | REST API call (`/services/server/info`) | N/A | N/A |

### 3. How much Splunk resource will this use?

#### Per-Query Impact

| Metric | Value | Comparison |
|--------|-------|------------|
| **Time range per query** | 1h (default) to 24h (max default) | Same as one UI search |
| **Results returned** | 50–100 max | Splunk Web default is 100 |
| **Search mode** | `normal` (batch) | NOT real-time |
| **Concurrent searches** | 1 per user session | Sequential, not parallel |
| **Query complexity** | Simple `search`, `stats`, field filters | No `join`, `transaction`, `collect` |

#### Expected Load Profile

| Scenario | Queries/Minute | Equivalent To |
|----------|---------------|---------------|
| **Single developer** using AI chat | 2–5 | One person using Splunk Web |
| **10 developers** actively chatting | 20–50 | 10 people using Splunk Web |
| **Peak usage** (incident response) | 50–100 | Small team in a war room |
| **Off-hours / idle** | 0 | No background polling or scheduled searches |

> **Bottom line**: At maximum expected usage (full dev team actively chatting), the load is
> equivalent to **10–20 users in the Splunk Web UI**. Enterprise Splunk deployments typically
> handle hundreds of concurrent users.

#### What This Integration Does NOT Do

- ❌ No **real-time searches** (no `rt_` prefix, no live tailing)
- ❌ No **scheduled searches** or saved reports
- ❌ No **data ingestion** or writing to Splunk indexes
- ❌ No **summary indexing** or `collect` commands
- ❌ No **dashboard or report creation**
- ❌ No **accelerated data models** or `tstats` on large datasets
- ❌ No **long-running searches** (all have timeouts)
- ❌ No **export** or bulk data extraction
- ❌ No **cross-index joins** or expensive `transaction` commands

### 4. What permissions does the service account need?

**Read-only access** to the following:

| Permission | Purpose | Splunk Role |
|------------|---------|-------------|
| `search` | Run SPL queries | `user` role |
| `list_indexes` | Discover available indexes | `user` role |
| `list_saved_searches` | List existing saved searches | `user` role |
| `get_server_info` | Health check | `user` role |

**The service account does NOT need:**
- ❌ `admin` role
- ❌ `can_delete` capability
- ❌ Write access to any index
- ❌ Access to `_internal`, `_audit`, or system indexes
- ❌ Ability to create/modify alerts, dashboards, or saved searches
- ❌ User management capabilities

#### Recommended Splunk Role Configuration

```
[role_gdc_mcp_readonly]
importRoles = user
srchIndexesAllowed = your_k8s_index;your_app_index
srchIndexesDefault = your_k8s_index
srchJobsQuota = 3
srchDiskQuota = 100
cumulativeSrchJobsQuota = 5
srchMaxTime = 300
```

| Setting | Value | Why |
|---------|-------|-----|
| `srchIndexesAllowed` | Only your app indexes | Prevents scanning unrelated data |
| `srchJobsQuota` | 3 | Max concurrent searches per user |
| `cumulativeSrchJobsQuota` | 5 | Max total active searches |
| `srchMaxTime` | 300 (5 min) | Auto-cancel long-running queries |
| `srchDiskQuota` | 100 MB | Limits temp disk usage for search results |

### 5. What safeguards prevent runaway queries?

#### Application-Level Controls (Built Into Our Code)

| Safeguard | Implementation | Effect |
|-----------|---------------|--------|
| **Result cap** | `max_results=100` in all search calls | Splunk stops scanning after hitting cap |
| **Time range defaults** | `-1h` for logs, `-24h` for error summaries | Prevents full-index scans |
| **Agent loop limit** | Max 5 tool calls per chat turn | Cannot fire unlimited queries |
| **Query timeout** | 30s HTTP timeout on MCP server | Prevents indefinitely hanging searches |
| **Job cleanup** | `job.cancel()` after reading results | Frees Splunk resources immediately |
| **Connection pooling** | Single persistent connection per MCP pod | No connection storms |
| **Normal search mode** | `search_mode='normal'` (not `realtime`) | Uses standard Splunk scheduling |

#### Splunk-Side Controls (Recommended)

| Control | How to Set | Effect |
|---------|-----------|--------|
| **Search quota** | `srchJobsQuota = 3` in role | Limits concurrent searches |
| **Max search time** | `srchMaxTime = 300` in role | Auto-kills queries after 5 min |
| **Index restriction** | `srchIndexesAllowed` in role | Only allow specific indexes |
| **Disk quota** | `srchDiskQuota = 100` in role | Limits temp storage |

### 6. What authentication method do you need?

We support **two authentication methods** (either works):

#### Option A: Splunk API Token (Recommended)

```
SPLUNK_TOKEN=<your-token-here>
```

- More secure (no password stored)
- Can be scoped and rotated
- Token-based auth doesn't require management port password access

#### Option B: Username + Password

```
SPLUNK_USERNAME=gdc-mcp-sa
SPLUNK_PASSWORD=<password>
```

- Traditional auth via Splunk management API
- Stored as Kubernetes Secret in our namespace

#### How Credentials Are Stored

Credentials are stored as a **Kubernetes Secret** in our GDC namespace and injected as environment
variables into the MCP server pod. They are:

- Never logged (our code masks credentials in diagnostic output)
- Never sent to the AI model or users
- Never exposed via API endpoints
- Encrypted at rest by GDC's etcd encryption

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: splunk-mcp-credentials
type: Opaque
data:
  SPLUNK_TOKEN: <base64-encoded-token>
```

### 7. What network access is required?

| Source | Destination | Port | Protocol | Purpose |
|--------|------------|------|----------|---------|
| Splunk MCP pod (GDC) | Splunk management API | **8089** | HTTPS | SDK queries, auth |

- **One-directional**: GDC → Splunk only. Splunk never calls back to GDC.
- **Single port**: Only port 8089 (REST API). Not port 8000 (Web UI).
- **HTTPS**: All communication is encrypted in transit.

### 8. How can you monitor our usage?

The Splunk platform team can monitor our service account's activity using:

```spl
# Search activity from the service account
index=_audit action=search user=gdc-mcp-sa
| stats count by search, earliest_time, latest_time, total_run_time
| sort -total_run_time

# Concurrent search count
index=_internal sourcetype=scheduler user=gdc-mcp-sa
| timechart count

# Resource usage
index=_internal source=*metrics.log group=search_concurrency user=gdc-mcp-sa
| timechart avg(active_searches) max(active_searches)
```

We recommend setting up a **Splunk alert** if the service account exceeds expected thresholds:

```spl
index=_audit action=search user=gdc-mcp-sa
| bin _time span=1m
| stats count by _time
| where count > 50
```

### 9. What happens if Splunk is unavailable?

The integration **degrades gracefully**:

1. The MCP server catches the connection error
2. Returns a friendly message: *"Splunk MCP connection error: ..."*
3. The AI agent tells the developer and suggests alternatives (e.g., K8s pod logs)
4. All other dashboard features (K8s tools, deployments, etc.) continue working normally

**No retry storms** — failed connections are not retried automatically. The user must send a new
chat message to trigger another attempt.

### 10. Can you restrict which indexes are searched?

**Yes.** This can be controlled at two levels:

1. **Splunk role** (`srchIndexesAllowed`): Restricts the service account to specific indexes
2. **MCP server config** (`SPLUNK_INDEX` env var): Sets a default index for all queries

We recommend restricting to only the indexes containing your team's application logs.

### 11. What is the service account naming convention?

We suggest: **`gdc-mcp-sa`** or **`svc-gdc-dashboard-readonly`**

This clearly indicates:
- It's a service account (not a person)
- It's for the GDC Dashboard
- It has read-only access

### 12. What is your data retention / compliance stance?

- **No data is stored** by the MCP server. It's a stateless proxy — results pass through and are not cached or persisted.
- **No data leaves the network**. Results flow from Splunk → MCP Server → AI Model (Vertex AI in GCP) → Dashboard.
- **Audit trail**: All queries are logged in Splunk's `_audit` index under the service account.
- **No PII extraction**: The AI summarizes log data but does not extract or store personally identifiable information.

---

## Summary for Approval

| Question | Answer |
|----------|--------|
| What access do you need? | Read-only search on specific indexes via port 8089 |
| How many queries? | 2–5 per developer interaction (equivalent to one UI user) |
| Max concurrent searches? | 3 (enforced by role quota) |
| Real-time searches? | No |
| Scheduled searches? | No |
| Data ingestion? | No |
| Write access? | No |
| Time range? | Default 1h–24h, never full-index scans |
| Max results per query? | 50–100 (hard-coded) |
| Credentials storage? | Kubernetes Secret (encrypted at rest) |
| Monitoring? | Full visibility via `_audit` index |
| Failure mode? | Graceful degradation, no retry storms |

---

## Contact

For questions about this integration, contact the GDC Dashboard team.
