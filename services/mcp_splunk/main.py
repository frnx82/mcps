#!/usr/bin/env python3
"""Splunk MCP Server — Exposes Splunk search as MCP tools over HTTP.

Implements the MCP (Model Context Protocol) JSON-RPC interface using only
the Python standard library + Flask (no fastmcp dependency needed).

Supports two modes:
  - Production: Connects to a real Splunk instance via splunk-sdk
  - Mock: Generates realistic K8s pod logs for development/demos

Usage:
  python main.py          # Production mode (requires SPLUNK_INSTANCE)
  python main.py --mock   # Mock mode (no Splunk needed)
"""

import os
import sys
import json
import random
import datetime
import uuid
import re
from typing import Optional
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# ══════════════════════════════════════════════════════════════════════════════
# Configuration
# ══════════════════════════════════════════════════════════════════════════════

SPLUNK_INSTANCE = os.getenv('SPLUNK_INSTANCE', '')
SPLUNK_PORT = int(os.getenv('SPLUNK_PORT', '8089'))
SPLUNK_SCHEME = os.getenv('SPLUNK_SCHEME', 'https')
SPLUNK_TOKEN = os.getenv('SPLUNK_TOKEN', '')
SPLUNK_USERNAME = os.getenv('SPLUNK_USERNAME', '')
SPLUNK_PASSWORD = os.getenv('SPLUNK_PASSWORD', '')
SPLUNK_DEFAULT_INDEX = os.getenv('SPLUNK_INDEX', 'main')
MCP_PORT = int(os.getenv('PORT', '8080'))
MOCK_MODE = os.getenv('MOCK_MODE', 'false').lower() in ('true', '1', 'yes')

# Check for --mock flag
if '--mock' in sys.argv:
    MOCK_MODE = True

# ══════════════════════════════════════════════════════════════════════════════
# Splunk Client (Production)
# ══════════════════════════════════════════════════════════════════════════════

_splunk_service = None


def _get_splunk_service():
    """Get or create a Splunk SDK service connection."""
    global _splunk_service
    if _splunk_service is not None:
        return _splunk_service

    # ── Diagnostic: log connection parameters ──────────────────────────
    masked_token = (SPLUNK_TOKEN[:4] + '****') if SPLUNK_TOKEN else '(not set)'
    masked_pass = ('****' + SPLUNK_PASSWORD[-2:]) if SPLUNK_PASSWORD else '(not set)'
    print(f"[splunk-mcp] ── Connection Diagnostics ──")
    print(f"[splunk-mcp]   SPLUNK_INSTANCE:  '{SPLUNK_INSTANCE}' {'⚠️ EMPTY!' if not SPLUNK_INSTANCE else ''}")
    print(f"[splunk-mcp]   SPLUNK_PORT:      {SPLUNK_PORT}")
    print(f"[splunk-mcp]   SPLUNK_SCHEME:    {SPLUNK_SCHEME}")
    print(f"[splunk-mcp]   SPLUNK_TOKEN:     {masked_token}")
    print(f"[splunk-mcp]   SPLUNK_USERNAME:  '{SPLUNK_USERNAME or '(not set)'}'")
    print(f"[splunk-mcp]   SPLUNK_PASSWORD:  {masked_pass}")
    print(f"[splunk-mcp]   Auth method:      {'Token' if SPLUNK_TOKEN else 'User/Pass' if SPLUNK_USERNAME else 'NONE ⚠️'}")

    # ── Diagnostic: test network connectivity before SDK login ────────
    import socket
    try:
        sock = socket.create_connection((SPLUNK_INSTANCE, SPLUNK_PORT), timeout=10)
        sock.close()
        print(f"[splunk-mcp]   Network check:    ✅ {SPLUNK_INSTANCE}:{SPLUNK_PORT} reachable")
    except Exception as net_err:
        print(f"[splunk-mcp]   Network check:    ❌ Cannot reach {SPLUNK_INSTANCE}:{SPLUNK_PORT}: {net_err}")
        raise ConnectionError(
            f"Cannot reach Splunk at {SPLUNK_INSTANCE}:{SPLUNK_PORT}: {net_err}. "
            f"Check SPLUNK_INSTANCE, SPLUNK_PORT, and network/firewall rules."
        )

    # ── Attempt SDK connection ────────────────────────────────────────
    try:
        import splunklib.client as client
        connect_args = {
            'host': SPLUNK_INSTANCE,
            'port': SPLUNK_PORT,
            'scheme': SPLUNK_SCHEME,
        }
        if SPLUNK_TOKEN:
            connect_args['splunkToken'] = SPLUNK_TOKEN
        elif SPLUNK_USERNAME and SPLUNK_PASSWORD:
            connect_args['username'] = SPLUNK_USERNAME
            connect_args['password'] = SPLUNK_PASSWORD
        else:
            raise ValueError("No Splunk credentials: set SPLUNK_TOKEN or SPLUNK_USERNAME + SPLUNK_PASSWORD")

        print(f"[splunk-mcp]   Connecting to {SPLUNK_SCHEME}://{SPLUNK_INSTANCE}:{SPLUNK_PORT} ...")
        _splunk_service = client.connect(**connect_args)
        print(f"[splunk-mcp] ✅ Connected to Splunk at {SPLUNK_SCHEME}://{SPLUNK_INSTANCE}:{SPLUNK_PORT}")
        return _splunk_service
    except Exception as e:
        import traceback
        print(f"[splunk-mcp] ❌ Failed to connect to Splunk: {e}")
        print(f"[splunk-mcp]    Error type: {type(e).__name__}")
        print(f"[splunk-mcp]    Full traceback:")
        traceback.print_exc()
        # Provide actionable hints based on error type
        err_str = str(e).lower()
        if 'xml' in err_str or 'sessionkey' in err_str or 'syntax error' in err_str:
            print(f"[splunk-mcp]    💡 HINT: Splunk returned an invalid login response.")
            print(f"[splunk-mcp]           This usually means wrong username/password,")
            print(f"[splunk-mcp]           or the Splunk server returned an error page.")
            print(f"[splunk-mcp]           Verify credentials: kubectl get secret splunk-mcp-credentials -o yaml")
        elif 'ssl' in err_str or 'certificate' in err_str:
            print(f"[splunk-mcp]    💡 HINT: TLS/SSL error. Try setting SPLUNK_SCHEME=http")
            print(f"[splunk-mcp]           or check if the Splunk cert is self-signed.")
        elif 'refused' in err_str or 'timeout' in err_str:
            print(f"[splunk-mcp]    💡 HINT: Network error. Check firewall rules between")
            print(f"[splunk-mcp]           GDC cluster and Splunk ({SPLUNK_INSTANCE}:{SPLUNK_PORT}).")
        raise


def _run_splunk_search(query, earliest='-1h', latest='now', max_results=100):
    """Run a Splunk search and return results as list of dicts."""
    import splunklib.results as results
    import time as _time

    service = _get_splunk_service()
    kwargs = {
        'earliest_time': earliest,
        'latest_time': latest,
        'search_mode': 'normal',
        'count': max_results,
    }

    # Ensure query starts with 'search'
    if not query.strip().startswith('|') and not query.strip().startswith('search '):
        query = f'search {query}'

    job = service.jobs.create(query, **kwargs)
    while not job.is_done():
        _time.sleep(0.5)

    rows = []
    for result in results.JSONResultsReader(job.results(output_mode='json', count=max_results)):
        if isinstance(result, dict):
            rows.append(result)

    job.cancel()
    return rows


# ══════════════════════════════════════════════════════════════════════════════
# Mock Data Generator
# ══════════════════════════════════════════════════════════════════════════════

MOCK_SERVICES = [
    'billing-service', 'payment-gateway', 'auth-service', 'user-service',
    'order-service', 'notification-service', 'inventory-service',
    'api-gateway', 'config-service', 'audit-service', 'report-service',
    'data-pipeline', 'cache-manager', 'scheduler-service', 'webhook-handler',
]

MOCK_NAMESPACES = ['uat', 'prod', 'staging']
MOCK_LOG_LEVELS = ['INFO', 'WARN', 'ERROR', 'DEBUG']
MOCK_LOG_WEIGHTS = [60, 15, 10, 15]

MOCK_CORRELATION_IDS = [
    'txn-a1b2c3d4-e5f6', 'txn-f7e8d9c0-b1a2', 'txn-1234abcd-5678',
    'req-9876fedc-ba98', 'req-aabb1122-3344', 'req-dead-beef-cafe',
    'trace-001122-aabbcc', 'trace-ddeeff-334455', 'trace-667788-990011',
    'corr-alpha-beta-001', 'corr-gamma-delta-002', 'corr-epsilon-zeta-003',
]

MOCK_LOG_TEMPLATES = {
    'INFO': [
        'Request processed successfully in {latency}ms',
        'User {user_id} authenticated via SSO',
        'Payment {payment_id} authorized — amount: ${amount}',
        'Cache hit for key: {cache_key} (TTL: {ttl}s)',
        'Health check passed — status: UP, db: connected, redis: connected',
        'Scheduled job {job_name} completed — processed {count} records',
        'Order {order_id} created — items: {count}, total: ${amount}',
        'Webhook delivered to {url} — status: 200, latency: {latency}ms',
        'Database connection pool: active={active}, idle={idle}, max={max}',
        'gRPC call to {service} completed in {latency}ms',
        'Kafka message published to topic {topic} — partition: {partition}, offset: {offset}',
        'Configuration reloaded from ConfigMap — {count} properties updated',
        'Session {session_id} created for user {user_id}',
        'Rate limiter: {count}/{max} requests in window — status: ALLOWED',
        'TLS certificate valid — expires in {days} days',
    ],
    'WARN': [
        'Slow query detected — table: {table}, duration: {latency}ms, rows: {count}',
        'Connection pool near capacity: {active}/{max} active connections',
        'Retry attempt {retry}/3 for downstream call to {service}',
        'Circuit breaker HALF-OPEN for {service} — testing with probe request',
        'Request rate approaching limit: {count}/{max} per minute',
        'Stale cache entry evicted for key: {cache_key} (age: {ttl}s)',
        'Memory usage at {pct}% — threshold: 85%',
        'Response time degradation: p99={latency}ms (SLA: 500ms)',
        'Deprecated API version v1 called by client {client_id} — migrate to v2',
        'DNS resolution slow: {latency}ms for {service}.svc.cluster.local',
    ],
    'ERROR': [
        'Connection refused to {service}:8080 — java.net.ConnectException: Connection refused',
        'NullPointerException at com.company.billing.PaymentProcessor.process(PaymentProcessor.java:142)',
        'Database query timeout after 30s — query: SELECT * FROM transactions WHERE created_at > ?',
        'OOMKilled: Container exceeded memory limit (512Mi) — current RSS: 524288Ki',
        'CrashLoopBackOff: Pod {pod_name} restarting — exit code 137 (OOMKilled)',
        'TLS handshake failed: certificate expired on 2026-05-15 — PKIX path validation failed',
        'Kafka consumer lag critical: topic={topic}, partition={partition}, lag={lag} messages',
        'HTTP 503 from {service} — upstream connect error: connection timeout',
        'Deadlock detected between threads Thread-12 and Thread-15 — transaction rolled back',
        'Disk space critical: /var/log at {pct}% — {free_mb}MB remaining',
        'Failed to parse JSON request body: Unexpected token at position 0',
        'Authentication failed for user {user_id}: invalid credentials (attempt {retry}/5)',
        'Redis connection lost: READONLY — failover in progress',
        'gRPC deadline exceeded: {service}/ProcessPayment — timeout: 5s',
        'OutOfMemoryError: Java heap space — consider increasing -Xmx from 256m',
    ],
    'DEBUG': [
        'Entering PaymentProcessor.process() — orderId={order_id}, amount=${amount}',
        'SQL: SELECT u.* FROM users u WHERE u.id = ? — params: [{user_id}]',
        'HTTP request: GET /api/v2/accounts/{user_id}/balance — headers: Accept: application/json',
        'Serializing response: {count} items, estimated size: {size}KB',
        'Cache lookup: key={cache_key}, result=MISS, fallback=database',
    ],
}

MOCK_INDEXES = [
    {'name': 'main', 'description': 'Primary application logs', 'currentDBSizeMB': 45200, 'totalEventCount': 892000000},
    {'name': 'prod_k8s', 'description': 'Production Kubernetes pod logs', 'currentDBSizeMB': 128400, 'totalEventCount': 3400000000},
    {'name': 'uat_k8s', 'description': 'UAT Kubernetes pod logs', 'currentDBSizeMB': 32100, 'totalEventCount': 670000000},
    {'name': 'security', 'description': 'Authentication and audit logs', 'currentDBSizeMB': 8900, 'totalEventCount': 245000000},
    {'name': 'metrics', 'description': 'Application and infrastructure metrics', 'currentDBSizeMB': 67300, 'totalEventCount': 5100000000},
    {'name': 'network', 'description': 'Network flow and firewall logs', 'currentDBSizeMB': 156000, 'totalEventCount': 8200000000},
]

MOCK_SAVED_SEARCHES = [
    {'name': 'Pod CrashLoopBackOff Alert', 'search': 'index=prod_k8s CrashLoopBackOff | stats count by pod_name', 'cron': '*/5 * * * *', 'description': 'Alerts on pods in CrashLoopBackOff state'},
    {'name': 'Error Rate by Service', 'search': 'index=prod_k8s level=ERROR | timechart span=5m count by service', 'cron': '*/10 * * * *', 'description': 'Tracks error rates across all services'},
    {'name': 'Slow Queries Report', 'search': 'index=main "Slow query" | stats avg(duration) max(duration) by table', 'cron': '0 * * * *', 'description': 'Hourly report of database slow queries'},
    {'name': 'OOM Events', 'search': 'index=prod_k8s (OOMKilled OR OutOfMemoryError) | stats count by pod_name, container', 'cron': '*/15 * * * *', 'description': 'Tracks out-of-memory kills'},
    {'name': 'Auth Failures Dashboard', 'search': 'index=security "Authentication failed" | stats count by user, source_ip', 'cron': '*/5 * * * *', 'description': 'Monitors authentication failures'},
    {'name': 'Daily Transaction Volume', 'search': 'index=main sourcetype=payment | timechart span=1h count', 'cron': '0 0 * * *', 'description': 'Daily summary of payment transactions'},
]


def _fill(template):
    """Fill a log template with random realistic values."""
    r = template
    reps = {
        '{latency}': str(random.choice([12, 45, 89, 156, 234, 567, 1023, 2340])),
        '{user_id}': f'user-{random.randint(1000, 9999)}',
        '{payment_id}': f'PAY-{random.randint(100000, 999999)}',
        '{order_id}': f'ORD-{random.randint(10000, 99999)}',
        '{amount}': f'{random.uniform(10, 5000):.2f}',
        '{cache_key}': random.choice(['user:profile:1234', 'product:detail:5678', 'session:abc123']),
        '{ttl}': str(random.choice([30, 60, 300, 600, 3600])),
        '{job_name}': random.choice(['daily-reconciliation', 'etl-pipeline', 'report-generator']),
        '{count}': str(random.randint(1, 5000)),
        '{url}': f'https://hooks.company.com/notify/{random.randint(100, 999)}',
        '{active}': str(random.randint(5, 45)),
        '{idle}': str(random.randint(2, 15)),
        '{max}': str(random.choice([50, 100, 200])),
        '{service}': random.choice(MOCK_SERVICES),
        '{topic}': random.choice(['payments.processed', 'orders.created', 'users.updated']),
        '{partition}': str(random.randint(0, 11)),
        '{offset}': str(random.randint(100000, 9999999)),
        '{session_id}': f'sess-{uuid.uuid4().hex[:12]}',
        '{table}': random.choice(['transactions', 'users', 'orders', 'audit_log']),
        '{retry}': str(random.randint(1, 3)),
        '{pct}': str(random.randint(70, 98)),
        '{client_id}': f'client-{random.randint(100, 999)}',
        '{pod_name}': f'{random.choice(MOCK_SERVICES)}-{random.choice("abcdef")}{random.randint(1,9)}',
        '{lag}': str(random.randint(100, 50000)),
        '{free_mb}': str(random.randint(50, 500)),
        '{days}': str(random.randint(1, 365)),
        '{size}': str(random.randint(1, 512)),
    }
    for k, v in reps.items():
        r = r.replace(k, v)
    return r


def _gen_logs(service=None, level=None, pattern=None, correlation_id=None,
              index=None, limit=50, earliest='-1h'):
    """Generate realistic mock K8s pod logs."""
    logs = []
    now = datetime.datetime.utcnow()

    hours_back = 1
    if earliest:
        m = re.match(r'-(\d+)([hmd])', earliest)
        if m:
            val, unit = int(m.group(1)), m.group(2)
            hours_back = val if unit == 'h' else (val / 60 if unit == 'm' else val * 24)

    services = [service] if service else random.sample(MOCK_SERVICES, min(8, len(MOCK_SERVICES)))

    for _ in range(min(limit * 3, 500)):
        svc = random.choice(services)
        ns = random.choice(MOCK_NAMESPACES)
        pod = f'{svc}-{random.choice("abcdef")}{random.randint(1,9)}{random.choice("wxyz")}{random.randint(10,99)}'
        ctr = svc.replace('-service', '').replace('-', '_')
        lvl = level.upper() if level else random.choices(MOCK_LOG_LEVELS, weights=MOCK_LOG_WEIGHTS, k=1)[0]
        msg = _fill(random.choice(MOCK_LOG_TEMPLATES.get(lvl, MOCK_LOG_TEMPLATES['INFO'])))
        cid = correlation_id if correlation_id else (random.choice(MOCK_CORRELATION_IDS) if random.random() < 0.3 else '')
        ts = now - datetime.timedelta(seconds=random.uniform(0, hours_back * 3600))

        logs.append({
            '_time': ts.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
            'host': f'k8s-node-{random.randint(1, 12)}.internal',
            'source': f'/var/log/pods/{ns}_{pod}/{ctr}/0.log',
            'sourcetype': 'kube:container:logs',
            'index': index or ('prod_k8s' if ns == 'prod' else 'uat_k8s'),
            'namespace': ns, 'pod_name': pod, 'container_name': ctr,
            'service': svc, 'level': lvl, 'correlation_id': cid,
            'message': msg,
            '_raw': f'{ts.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]}Z {lvl:5s} [{ctr}] '
                     + (f'[{cid}] ' if cid else '') + msg,
        })

    logs.sort(key=lambda x: x['_time'], reverse=True)
    if pattern:
        pl = pattern.lower()
        logs = [l for l in logs if pl in l['message'].lower() or pl in l.get('service', '').lower()]
    if correlation_id:
        logs = [l for l in logs if l.get('correlation_id') == correlation_id]
    return logs[:limit]


def _gen_error_summary(service=None, index=None, earliest='-24h'):
    """Generate mock error summary."""
    services = [service] if service else random.sample(MOCK_SERVICES, 6)
    total_e, total_err = 0, 0
    svc_list = []
    for svc in services:
        events = random.randint(5000, 150000)
        errors = random.randint(0, int(events * 0.08))
        warns = random.randint(0, int(events * 0.15))
        top_errors = [{'message': _fill(t)[:120], 'count': random.randint(1, max(1, errors // 3)),
                       'first_seen': (datetime.datetime.utcnow() - datetime.timedelta(hours=random.randint(1, 24))).isoformat() + 'Z',
                       'last_seen': (datetime.datetime.utcnow() - datetime.timedelta(minutes=random.randint(1, 60))).isoformat() + 'Z'}
                      for t in random.sample(MOCK_LOG_TEMPLATES['ERROR'], min(3, len(MOCK_LOG_TEMPLATES['ERROR'])))]
        svc_list.append({'service': svc, 'total_events': events, 'error_count': errors,
                         'warn_count': warns, 'error_rate_pct': round(errors / events * 100, 2) if events else 0,
                         'top_errors': sorted(top_errors, key=lambda x: x['count'], reverse=True)})
        total_e += events
        total_err += errors
    svc_list.sort(key=lambda x: x['error_count'], reverse=True)
    return {'time_range': earliest, 'total_events': total_e, 'total_errors': total_err,
            'error_rate_pct': round(total_err / total_e * 100, 2) if total_e else 0, 'services': svc_list}


def _gen_correlation_trace(correlation_id, earliest='-24h'):
    """Generate a realistic distributed trace for a correlation ID."""
    trace_services = random.sample(MOCK_SERVICES, random.randint(3, 6))
    now = datetime.datetime.utcnow()
    logs = []
    base_time = now - datetime.timedelta(minutes=random.randint(5, 120))
    cumulative_ms = 0

    for i, svc in enumerate(trace_services):
        latency = random.randint(5, 200)
        cumulative_ms += latency
        ts = base_time + datetime.timedelta(milliseconds=cumulative_ms)
        pod = f'{svc}-{random.choice("abcdef")}{random.randint(1,9)}{random.choice("wxyz")}{random.randint(10,99)}'
        ctr = svc.replace('-service', '').replace('-', '_')
        prev = trace_services[i - 1] if i > 0 else 'api-gateway'

        logs.append({
            '_time': ts.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
            'host': f'k8s-node-{random.randint(1, 12)}.internal',
            'source': f'/var/log/pods/prod_{pod}/{ctr}/0.log',
            'sourcetype': 'kube:container:logs', 'namespace': 'prod',
            'pod_name': pod, 'container_name': ctr, 'service': svc,
            'level': 'INFO', 'correlation_id': correlation_id,
            'message': f'Received request from {prev} — processing',
            '_raw': f'{ts.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]}Z INFO  [{ctr}] [{correlation_id}] Received request from {prev}',
        })

        # Maybe inject an error
        if i == len(trace_services) - 2 and random.random() < 0.4:
            err_ts = ts + datetime.timedelta(milliseconds=random.randint(10, 50))
            err_msg = _fill(random.choice(MOCK_LOG_TEMPLATES['ERROR']))
            logs.append({
                '_time': err_ts.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
                'host': f'k8s-node-{random.randint(1, 12)}.internal',
                'source': f'/var/log/pods/prod_{pod}/{ctr}/0.log',
                'sourcetype': 'kube:container:logs', 'namespace': 'prod',
                'pod_name': pod, 'container_name': ctr, 'service': svc,
                'level': 'ERROR', 'correlation_id': correlation_id,
                'message': err_msg,
                '_raw': f'{err_ts.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]}Z ERROR [{ctr}] [{correlation_id}] {err_msg}',
            })

        done_ts = ts + datetime.timedelta(milliseconds=latency)
        nxt = trace_services[i + 1] if i < len(trace_services) - 1 else 'response'
        logs.append({
            '_time': done_ts.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
            'host': f'k8s-node-{random.randint(1, 12)}.internal',
            'source': f'/var/log/pods/prod_{pod}/{ctr}/0.log',
            'sourcetype': 'kube:container:logs', 'namespace': 'prod',
            'pod_name': pod, 'container_name': ctr, 'service': svc,
            'level': 'INFO', 'correlation_id': correlation_id,
            'message': f'Completed — latency: {latency}ms, forwarding to {nxt}',
            '_raw': f'{done_ts.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]}Z INFO  [{ctr}] [{correlation_id}] Completed — {latency}ms → {nxt}',
        })

    logs.sort(key=lambda x: x['_time'])
    return {
        'correlation_id': correlation_id,
        'log_count': len(logs),
        'service_chain': ' → '.join(trace_services),
        'services_involved': trace_services,
        'total_latency_ms': cumulative_ms,
        'logs': logs,
    }


# ══════════════════════════════════════════════════════════════════════════════
# MCP Tool Registry
# ══════════════════════════════════════════════════════════════════════════════

TOOLS = {
    'splunk_search': {
        'description': 'Run an arbitrary SPL (Splunk Processing Language) query and return results.',
        'inputSchema': {
            'type': 'object',
            'properties': {
                'query': {'type': 'string', 'description': 'SPL query string'},
                'earliest': {'type': 'string', 'description': 'Time range start (e.g. -1h, -24h, -7d)', 'default': '-1h'},
                'latest': {'type': 'string', 'description': 'Time range end', 'default': 'now'},
                'max_results': {'type': 'integer', 'description': 'Max results', 'default': 100},
                'index': {'type': 'string', 'description': 'Splunk index to search'},
            },
            'required': ['query'],
        },
    },
    'splunk_get_pod_logs': {
        'description': 'Get Kubernetes pod logs for a specific service, optionally filtered by pattern, log level, or namespace.',
        'inputSchema': {
            'type': 'object',
            'properties': {
                'service': {'type': 'string', 'description': 'Service/pod name (e.g. billing-service)'},
                'pattern': {'type': 'string', 'description': 'Text pattern to search in logs (e.g. timeout, NullPointer)'},
                'level': {'type': 'string', 'description': 'Log level filter: ERROR, WARN, INFO, DEBUG'},
                'namespace': {'type': 'string', 'description': 'K8s namespace (e.g. prod, uat)'},
                'limit': {'type': 'integer', 'description': 'Max log entries', 'default': 50},
                'earliest': {'type': 'string', 'description': 'Time range start', 'default': '-1h'},
                'index': {'type': 'string', 'description': 'Splunk index'},
            },
            'required': ['service'],
        },
    },
    'splunk_search_by_correlation_id': {
        'description': 'Trace a request across all services by correlation/trace ID. Shows the full journey of a request through microservices.',
        'inputSchema': {
            'type': 'object',
            'properties': {
                'correlation_id': {'type': 'string', 'description': 'Correlation ID, trace ID, or request ID'},
                'earliest': {'type': 'string', 'description': 'How far back to search', 'default': '-24h'},
                'limit': {'type': 'integer', 'description': 'Max results', 'default': 100},
                'index': {'type': 'string', 'description': 'Splunk index'},
            },
            'required': ['correlation_id'],
        },
    },
    'splunk_get_error_summary': {
        'description': 'Get error rate summary and top errors for a service or all services.',
        'inputSchema': {
            'type': 'object',
            'properties': {
                'service': {'type': 'string', 'description': 'Service name (omit for all services)'},
                'earliest': {'type': 'string', 'description': 'Time range', 'default': '-24h'},
                'index': {'type': 'string', 'description': 'Splunk index'},
            },
        },
    },
    'splunk_list_indexes': {
        'description': 'List all available Splunk indexes with size and event counts.',
        'inputSchema': {'type': 'object', 'properties': {}},
    },
    'splunk_get_saved_searches': {
        'description': 'List saved searches and reports configured in Splunk.',
        'inputSchema': {'type': 'object', 'properties': {}},
    },
    'splunk_health': {
        'description': 'Check Splunk connection health and server info.',
        'inputSchema': {'type': 'object', 'properties': {}},
    },
}


def _handle_tool_call(tool_name, arguments):
    """Dispatch a tool call and return the result string."""

    if tool_name == 'splunk_search':
        q = arguments.get('query', '')
        if MOCK_MODE:
            svc, lvl, pat = None, None, None
            ql = q.lower()
            for s in MOCK_SERVICES:
                if s in ql:
                    svc = s; break
            for l in ['ERROR', 'WARN', 'INFO', 'DEBUG']:
                if f'level={l.lower()}' in ql or f'level="{l}"' in ql:
                    lvl = l; break
            quoted = re.findall(r'"([^"]+)"', q)
            for qv in quoted:
                if qv not in MOCK_SERVICES and qv.upper() not in MOCK_LOG_LEVELS:
                    pat = qv; break
            logs = _gen_logs(service=svc, level=lvl, pattern=pat,
                             index=arguments.get('index'), limit=arguments.get('max_results', 100),
                             earliest=arguments.get('earliest', '-1h'))
            return json.dumps({'results': logs, 'result_count': len(logs), 'query': q, 'mode': 'mock'})
        else:
            idx = arguments.get('index', SPLUNK_DEFAULT_INDEX)
            if 'index=' not in q.lower():
                q = f'index={idx} {q}'
            results = _run_splunk_search(q, earliest=arguments.get('earliest', '-1h'),
                                          latest=arguments.get('latest', 'now'),
                                          max_results=arguments.get('max_results', 100))
            return json.dumps({'results': results, 'result_count': len(results), 'query': q})

    elif tool_name == 'splunk_get_pod_logs':
        svc = arguments.get('service', '')
        if MOCK_MODE:
            logs = _gen_logs(service=svc, level=arguments.get('level'), pattern=arguments.get('pattern'),
                             index=arguments.get('index'), limit=arguments.get('limit', 50),
                             earliest=arguments.get('earliest', '-1h'))
            ns = arguments.get('namespace')
            if ns:
                logs = [l for l in logs if l.get('namespace') == ns]
            return json.dumps({'service': svc, 'log_count': len(logs),
                               'filters': {k: arguments.get(k) for k in ('pattern', 'level', 'namespace', 'earliest')},
                               'logs': logs, 'mode': 'mock'})
        else:
            idx = arguments.get('index', SPLUNK_DEFAULT_INDEX)
            parts = [f'index={idx}', f'"{svc}"']
            if arguments.get('namespace'): parts.append(f'namespace="{arguments["namespace"]}"')
            if arguments.get('level'): parts.append(f'level="{arguments["level"].upper()}"')
            if arguments.get('pattern'): parts.append(f'"{arguments["pattern"]}"')
            lim = arguments.get('limit', 50)
            parts.append(f'| head {lim}')
            results = _run_splunk_search(' '.join(parts), earliest=arguments.get('earliest', '-1h'), max_results=lim)
            return json.dumps({'service': svc, 'log_count': len(results), 'logs': results})

    elif tool_name == 'splunk_search_by_correlation_id':
        cid = arguments.get('correlation_id', '')
        if MOCK_MODE:
            trace = _gen_correlation_trace(cid, arguments.get('earliest', '-24h'))
            trace['mode'] = 'mock'
            return json.dumps(trace)
        else:
            idx_clause = f'index={arguments["index"]}' if arguments.get('index') else 'index=*'
            lim = arguments.get('limit', 100)
            results = _run_splunk_search(f'{idx_clause} "{cid}" | sort _time | head {lim}',
                                          earliest=arguments.get('earliest', '-24h'), max_results=lim)
            svcs = list(set(r.get('service', '?') for r in results))
            return json.dumps({'correlation_id': cid, 'log_count': len(results), 'services_involved': svcs, 'logs': results})

    elif tool_name == 'splunk_get_error_summary':
        if MOCK_MODE:
            s = _gen_error_summary(service=arguments.get('service'), earliest=arguments.get('earliest', '-24h'))
            s['mode'] = 'mock'
            return json.dumps(s)
        else:
            idx = arguments.get('index', SPLUNK_DEFAULT_INDEX)
            svc = arguments.get('service')
            if svc:
                q = f'index={idx} "{svc}" | stats count as total, count(eval(level="ERROR")) as errors by service'
            else:
                q = f'index={idx} level=ERROR | stats count by service | sort -count | head 20'
            results = _run_splunk_search(q, earliest=arguments.get('earliest', '-24h'))
            return json.dumps({'service': svc or 'all', 'results': results})

    elif tool_name == 'splunk_list_indexes':
        if MOCK_MODE:
            return json.dumps({'indexes': MOCK_INDEXES, 'count': len(MOCK_INDEXES), 'mode': 'mock'})
        else:
            service = _get_splunk_service()
            idxs = [{'name': i.name, 'currentDBSizeMB': int(i['currentDBSizeMB']),
                      'totalEventCount': int(i['totalEventCount'])} for i in service.indexes]
            return json.dumps({'indexes': idxs, 'count': len(idxs)})

    elif tool_name == 'splunk_get_saved_searches':
        if MOCK_MODE:
            return json.dumps({'saved_searches': MOCK_SAVED_SEARCHES, 'count': len(MOCK_SAVED_SEARCHES), 'mode': 'mock'})
        else:
            service = _get_splunk_service()
            ss = [{'name': s.name, 'search': s['search'], 'cron': s.get('cron_schedule', '')} for s in service.saved_searches]
            return json.dumps({'saved_searches': ss, 'count': len(ss)})

    elif tool_name == 'splunk_health':
        if MOCK_MODE:
            return json.dumps({'status': 'healthy', 'connected': True, 'mode': 'mock',
                               'server_info': {'server_name': 'splunk-mock.internal', 'version': '9.2.1'},
                               'capabilities': list(TOOLS.keys())})
        else:
            try:
                service = _get_splunk_service()
                info = service.info
                return json.dumps({'status': 'healthy', 'connected': True,
                                   'server_info': {'server_name': info.get('serverName', '?'), 'version': info.get('version', '?')}})
            except Exception as e:
                return json.dumps({'status': 'unhealthy', 'connected': False, 'error': str(e)})

    return json.dumps({'error': f'Unknown tool: {tool_name}'})


# ══════════════════════════════════════════════════════════════════════════════
# HTTP Server (MCP JSON-RPC over HTTP)
# ══════════════════════════════════════════════════════════════════════════════

class MCPHandler(BaseHTTPRequestHandler):
    """Handle MCP JSON-RPC requests over HTTP."""

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            print(f"[splunk-mcp] ⚠️ Empty request body (Content-Length: 0)")
            self._send_json(200, {
                'jsonrpc': '2.0', 'id': '1',
                'error': {'code': -32700, 'message': 'Empty request body — Content-Length was 0'}
            })
            return

        body = self.rfile.read(content_length)

        try:
            request = json.loads(body)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"[splunk-mcp] ⚠️ JSON parse error: {e}")
            print(f"[splunk-mcp]    Body ({len(body)} bytes): {body[:300]}")
            self._send_json(200, {
                'jsonrpc': '2.0', 'id': '1',
                'error': {'code': -32700, 'message': f'Invalid JSON in request body: {e}'}
            })
            return

        req_id = request.get('id', '1')
        method = request.get('method', '')
        params = request.get('params', {})

        print(f"[splunk-mcp] {method} {json.dumps(params)[:200]}")

        if method == 'tools/list':
            tools_list = []
            for name, meta in TOOLS.items():
                tools_list.append({
                    'name': name,
                    'description': meta['description'],
                    'inputSchema': meta['inputSchema'],
                })
            self._send_json(200, {
                'jsonrpc': '2.0', 'id': req_id,
                'result': {'tools': tools_list},
            })

        elif method == 'tools/call':
            tool_name = params.get('name', '')
            arguments = params.get('arguments', {})

            if tool_name not in TOOLS:
                self._send_json(200, {
                    'jsonrpc': '2.0', 'id': req_id,
                    'error': {'code': -32601, 'message': f'Unknown tool: {tool_name}'},
                })
                return

            try:
                result_text = _handle_tool_call(tool_name, arguments)
                self._send_json(200, {
                    'jsonrpc': '2.0', 'id': req_id,
                    'result': {
                        'content': [{'type': 'text', 'text': result_text}],
                    },
                })
            except Exception as e:
                print(f"[splunk-mcp] ❌ Error in {tool_name}: {e}")
                import traceback
                traceback.print_exc()
                self._send_json(200, {
                    'jsonrpc': '2.0', 'id': req_id,
                    'error': {'code': -32000, 'message': str(e)},
                })

        elif method == 'initialize':
            self._send_json(200, {
                'jsonrpc': '2.0', 'id': req_id,
                'result': {
                    'protocolVersion': '2024-11-05',
                    'serverInfo': {'name': 'splunk-mcp-server', 'version': '1.0.0'},
                    'capabilities': {'tools': {'listChanged': False}},
                },
            })

        else:
            self._send_json(200, {
                'jsonrpc': '2.0', 'id': req_id,
                'error': {'code': -32601, 'message': f'Method not found: {method}'},
            })

    def do_GET(self):
        """Health check endpoint."""
        self._send_json(200, {
            'status': 'healthy',
            'server': 'splunk-mcp-server',
            'mode': 'mock' if MOCK_MODE else 'production',
            'tools': len(TOOLS),
        })

    def _send_json(self, code, data):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_OPTIONS(self):
        """CORS preflight."""
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def log_message(self, format, *args):
        """Suppress default HTTP logging (we have our own)."""
        pass


# ══════════════════════════════════════════════════════════════════════════════
# Entry Point
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    mode_str = '🧪 MOCK MODE' if MOCK_MODE else '🏭 PRODUCTION'
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║           Splunk MCP Server — {mode_str}              ║
╠══════════════════════════════════════════════════════════════╣
║  Transport: HTTP (JSON-RPC)                                  ║
║  Port:      {MCP_PORT:<47d}║
║  Tools:     {len(TOOLS)} ({', '.join(list(TOOLS.keys())[:3])}, ...)  ║
╚══════════════════════════════════════════════════════════════╝
""")

    if not MOCK_MODE:
        if not SPLUNK_INSTANCE:
            print("[splunk-mcp] ⚠️  SPLUNK_INSTANCE not set — use --mock for mock mode")
            sys.exit(1)
        print(f"[splunk-mcp] Splunk: {SPLUNK_SCHEME}://{SPLUNK_INSTANCE}:{SPLUNK_PORT}")
        auth = 'Token' if SPLUNK_TOKEN else 'User/Pass' if SPLUNK_USERNAME else 'None'
        print(f"[splunk-mcp] Auth:   {auth}")
    else:
        print(f"[splunk-mcp] Mock services: {len(MOCK_SERVICES)}")
        print(f"[splunk-mcp] Mock indexes:  {len(MOCK_INDEXES)}")

    print(f"[splunk-mcp] Starting on http://0.0.0.0:{MCP_PORT} ...")
    server = HTTPServer(('0.0.0.0', MCP_PORT), MCPHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[splunk-mcp] Shutting down.")
        server.shutdown()
