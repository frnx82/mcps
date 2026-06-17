"""Security module — SQL validation, injection protection, query guardrails."""

import re
import logging
from config import READ_ONLY, MAX_ROW_LIMIT

logger = logging.getLogger("mcp_database.security")

# ── Dangerous SQL patterns (for read-only mode) ──────────────────────────────
WRITE_KEYWORDS = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|TRUNCATE|CREATE|GRANT|REVOKE|MERGE|UPSERT|REPLACE)\b",
    re.IGNORECASE,
)

# ── SQL injection patterns ────────────────────────────────────────────────────
INJECTION_PATTERNS = [
    re.compile(r";\s*(DROP|DELETE|INSERT|UPDATE|ALTER|CREATE|TRUNCATE)", re.IGNORECASE),
    re.compile(r"--\s*$", re.MULTILINE),  # SQL line comments at end
    re.compile(r"/\*.*?\*/", re.DOTALL),  # Block comments (potential obfuscation)
    re.compile(r"\bUNION\s+ALL\s+SELECT\b", re.IGNORECASE),  # UNION injection
    re.compile(r"\bEXEC(UTE)?\s*\(", re.IGNORECASE),  # EXEC calls
    re.compile(r"\bxp_\w+", re.IGNORECASE),  # SQL Server extended procs
    re.compile(r"\bUTL_\w+", re.IGNORECASE),  # Oracle UTL packages
    re.compile(r"\bDBMS_\w+\.\w+", re.IGNORECASE),  # Oracle DBMS packages
]

# ── Multi-statement detection ─────────────────────────────────────────────────
MULTI_STATEMENT = re.compile(r";\s*\S", re.DOTALL)


class QueryValidationError(Exception):
    """Raised when a query fails security validation."""
    pass


def validate_query(sql: str, db_type: str = "generic") -> str:
    """Validate and sanitize a SQL query.

    Args:
        sql: The SQL query string to validate.
        db_type: The database type (oracle, impala, bigquery, cloudsql_pg, cloudsql_mysql).

    Returns:
        The validated (and possibly trimmed) SQL string.

    Raises:
        QueryValidationError: If the query fails validation.
    """
    if not sql or not sql.strip():
        raise QueryValidationError("Empty query")

    sql = sql.strip()

    # Remove trailing semicolons (common user habit)
    sql = sql.rstrip(";").strip()

    # ── Check for multi-statement queries ─────────────────────────────────
    if MULTI_STATEMENT.search(sql):
        raise QueryValidationError(
            "Multi-statement queries are not allowed. Please submit one query at a time."
        )

    # ── Read-only mode: block write operations ────────────────────────────
    if READ_ONLY:
        match = WRITE_KEYWORDS.search(sql)
        if match:
            raise QueryValidationError(
                f"Write operation '{match.group()}' is not allowed in read-only mode. "
                "Only SELECT and read-only queries are permitted."
            )

    # ── Check for SQL injection patterns ──────────────────────────────────
    for pattern in INJECTION_PATTERNS:
        if pattern.search(sql):
            logger.warning("Potential SQL injection detected in query: %s", sql[:200])
            raise QueryValidationError(
                "Query contains potentially dangerous patterns and was blocked for security."
            )

    # ── Query length limit ────────────────────────────────────────────────
    if len(sql) > 10_000:
        raise QueryValidationError(
            f"Query too long ({len(sql)} chars). Maximum allowed is 10,000 characters."
        )

    return sql


def enforce_row_limit(sql: str, limit: int, db_type: str = "generic") -> str:
    """Add or enforce a row limit on a SELECT query.

    Args:
        sql: The SQL query.
        limit: Desired row limit.
        db_type: Database type for dialect-specific LIMIT syntax.

    Returns:
        The SQL with a row limit applied.
    """
    limit = min(limit, MAX_ROW_LIMIT)

    # Check if query already has a LIMIT/FETCH/ROWNUM clause
    has_limit = re.search(
        r"\b(LIMIT|FETCH\s+FIRST|ROWNUM|TOP)\b", sql, re.IGNORECASE
    )

    if has_limit:
        return sql  # User already specified a limit, respect it

    # Only add LIMIT to SELECT queries
    if not re.match(r"\s*(SELECT|WITH)\b", sql, re.IGNORECASE):
        return sql

    if db_type == "oracle":
        # Oracle uses FETCH FIRST for 12c+, ROWNUM for older
        return f"{sql} FETCH FIRST {limit} ROWS ONLY"
    elif db_type == "bigquery":
        return f"{sql} LIMIT {limit}"
    elif db_type == "impala":
        return f"{sql} LIMIT {limit}"
    else:
        # PostgreSQL, MySQL — standard LIMIT
        return f"{sql} LIMIT {limit}"


def mask_credentials(text: str) -> str:
    """Remove any accidentally exposed credentials from error messages."""
    # Mask common credential patterns
    patterns = [
        (re.compile(r"(password\s*[=:]\s*)['\"]?[^'\";\s]+", re.IGNORECASE), r"\1****"),
        (re.compile(r"(token\s*[=:]\s*)['\"]?[^'\";\s]+", re.IGNORECASE), r"\1****"),
        (re.compile(r"(secret\s*[=:]\s*)['\"]?[^'\";\s]+", re.IGNORECASE), r"\1****"),
    ]
    for pattern, replacement in patterns:
        text = pattern.sub(replacement, text)
    return text
