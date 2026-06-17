"""Configuration for Multi-Database MCP Server.

All database connections are configured via environment variables.
"""

import os
import json
import logging

logger = logging.getLogger("mcp_database")

# ══════════════════════════════════════════════════════════════════════════════
# Server Configuration
# ══════════════════════════════════════════════════════════════════════════════

MCP_PORT = int(os.getenv("PORT", "8080"))
MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() in ("true", "1", "yes")
READ_ONLY = os.getenv("READ_ONLY", "true").lower() in ("true", "1", "yes")
DEFAULT_ROW_LIMIT = int(os.getenv("DEFAULT_ROW_LIMIT", "100"))
MAX_ROW_LIMIT = int(os.getenv("MAX_ROW_LIMIT", "1000"))
QUERY_TIMEOUT_SECONDS = int(os.getenv("QUERY_TIMEOUT_SECONDS", "30"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# ══════════════════════════════════════════════════════════════════════════════
# Database Configurations
# ══════════════════════════════════════════════════════════════════════════════


def _mask(value: str, show: int = 4) -> str:
    """Mask sensitive values for logging."""
    if not value:
        return "(not set)"
    if len(value) <= show:
        return "****"
    return value[:show] + "****"


class DatabaseConfig:
    """Configuration for a single database connection."""

    def __init__(self, name: str, db_type: str, **kwargs):
        self.name = name
        self.db_type = db_type  # oracle, impala, bigquery, cloudsql_pg, cloudsql_mysql
        self.params = kwargs
        self.enabled = kwargs.get("enabled", True)

    def __repr__(self):
        return f"DatabaseConfig(name={self.name!r}, type={self.db_type!r}, enabled={self.enabled})"


def load_database_configs() -> dict[str, DatabaseConfig]:
    """Load database configurations from environment variables."""
    configs = {}

    # ── Oracle (on-prem) ──────────────────────────────────────────────────
    if os.getenv("ORACLE_DSN") or os.getenv("ORACLE_HOST"):
        configs["oracle"] = DatabaseConfig(
            name="oracle",
            db_type="oracle",
            dsn=os.getenv("ORACLE_DSN", ""),
            host=os.getenv("ORACLE_HOST", ""),
            port=int(os.getenv("ORACLE_PORT", "1521")),
            service_name=os.getenv("ORACLE_SERVICE_NAME", ""),
            user=os.getenv("ORACLE_USER", ""),
            password=os.getenv("ORACLE_PASSWORD", ""),
            min_pool_size=int(os.getenv("ORACLE_MIN_POOL", "1")),
            max_pool_size=int(os.getenv("ORACLE_MAX_POOL", "5")),
        )
        logger.info(
            "Oracle configured: host=%s, user=%s",
            os.getenv("ORACLE_HOST", os.getenv("ORACLE_DSN", "")),
            _mask(os.getenv("ORACLE_USER", "")),
        )

    # ── Impala (on-prem) ──────────────────────────────────────────────────
    if os.getenv("IMPALA_HOST"):
        configs["impala"] = DatabaseConfig(
            name="impala",
            db_type="impala",
            host=os.getenv("IMPALA_HOST", ""),
            port=int(os.getenv("IMPALA_PORT", "21050")),
            auth_mechanism=os.getenv("IMPALA_AUTH_MECHANISM", "NOSASL"),  # NOSASL, PLAIN, GSSAPI, LDAP
            user=os.getenv("IMPALA_USER", ""),
            password=os.getenv("IMPALA_PASSWORD", ""),
            use_ssl=os.getenv("IMPALA_USE_SSL", "false").lower() in ("true", "1"),
            kerberos_service_name=os.getenv("IMPALA_KERBEROS_SERVICE_NAME", "impala"),
            database=os.getenv("IMPALA_DATABASE", "default"),
        )
        logger.info(
            "Impala configured: host=%s:%s, auth=%s",
            os.getenv("IMPALA_HOST"),
            os.getenv("IMPALA_PORT", "21050"),
            os.getenv("IMPALA_AUTH_MECHANISM", "NOSASL"),
        )

    # ── BigQuery (GCP) ────────────────────────────────────────────────────
    if os.getenv("BIGQUERY_PROJECT"):
        creds_path = os.getenv("BIGQUERY_CREDENTIALS_PATH", "")
        configs["bigquery"] = DatabaseConfig(
            name="bigquery",
            db_type="bigquery",
            project=os.getenv("BIGQUERY_PROJECT", ""),
            credentials_path=creds_path,
            location=os.getenv("BIGQUERY_LOCATION", "US"),
            dataset=os.getenv("BIGQUERY_DATASET", ""),
        )
        logger.info(
            "BigQuery configured: project=%s, location=%s",
            os.getenv("BIGQUERY_PROJECT"),
            os.getenv("BIGQUERY_LOCATION", "US"),
        )

    # ── CloudSQL (GCP) ────────────────────────────────────────────────────
    if os.getenv("CLOUDSQL_HOST") or os.getenv("CLOUDSQL_INSTANCE"):
        db_engine = os.getenv("CLOUDSQL_TYPE", "postgres").lower()
        db_type = "cloudsql_pg" if db_engine in ("postgres", "postgresql") else "cloudsql_mysql"
        configs["cloudsql"] = DatabaseConfig(
            name="cloudsql",
            db_type=db_type,
            host=os.getenv("CLOUDSQL_HOST", "127.0.0.1"),  # Cloud SQL Proxy
            port=int(os.getenv("CLOUDSQL_PORT", "5432" if "pg" in db_type else "3306")),
            user=os.getenv("CLOUDSQL_USER", ""),
            password=os.getenv("CLOUDSQL_PASSWORD", ""),
            database=os.getenv("CLOUDSQL_DATABASE", ""),
            instance=os.getenv("CLOUDSQL_INSTANCE", ""),  # project:region:instance
        )
        logger.info(
            "CloudSQL configured: type=%s, host=%s, database=%s",
            db_engine,
            os.getenv("CLOUDSQL_HOST", "127.0.0.1"),
            os.getenv("CLOUDSQL_DATABASE", ""),
        )

    return configs
