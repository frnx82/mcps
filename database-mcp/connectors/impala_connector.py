"""Impala Database Connector — uses impyla (HiveServer2 protocol)."""

import time
import logging
from typing import Optional, Any

from connectors import BaseConnector, QueryResult, TableInfo, ColumnInfo

logger = logging.getLogger("mcp_database.impala")


class ImpalaConnector(BaseConnector):
    """Connector for Apache Impala (on-prem).

    Uses impyla library via HiveServer2 protocol.
    Supports NOSASL, LDAP, PLAIN, and GSSAPI (Kerberos) authentication.
    """

    def __init__(self, name: str, config: dict):
        super().__init__(name, "impala", config)
        self._conn = None

    def connect(self) -> None:
        try:
            from impala.dbapi import connect

            connect_kwargs = {
                "host": self.config.get("host", "localhost"),
                "port": int(self.config.get("port", 21050)),
                "auth_mechanism": self.config.get("auth_mechanism", "NOSASL"),
                "database": self.config.get("database", "default"),
            }

            auth = connect_kwargs["auth_mechanism"]
            if auth in ("PLAIN", "LDAP"):
                connect_kwargs["user"] = self.config.get("user", "")
                connect_kwargs["password"] = self.config.get("password", "")
            elif auth == "GSSAPI":
                connect_kwargs["kerberos_service_name"] = self.config.get(
                    "kerberos_service_name", "impala"
                )

            if self.config.get("use_ssl"):
                connect_kwargs["use_ssl"] = True

            self._conn = connect(**connect_kwargs)
            self._connected = True
            logger.info("Impala connected: %s (%s:%s)", self.name,
                        self.config.get("host"), self.config.get("port"))
        except Exception as e:
            logger.error("Failed to connect to Impala '%s': %s", self.name, e)
            self._connected = False
            raise

    def disconnect(self) -> None:
        if self._conn:
            try:
                self._conn.close()
            except Exception:
                pass
            self._conn = None
        self._connected = False
        logger.info("Impala connection closed: %s", self.name)

    def execute(self, sql: str, params: Optional[dict] = None) -> QueryResult:
        start = time.monotonic()
        cursor = self._conn.cursor()
        try:
            cursor.execute(sql)

            if cursor.description:
                columns = [col[0] for col in cursor.description]
                rows = []
                for row in cursor:
                    rows.append([self._serialize_value(v) for v in row])
                return QueryResult(
                    columns=columns,
                    rows=rows,
                    row_count=len(rows),
                    database=self.name,
                    query=sql,
                    execution_time_ms=(time.monotonic() - start) * 1000,
                )
            else:
                return QueryResult(
                    columns=[],
                    rows=[],
                    row_count=0,
                    database=self.name,
                    query=sql,
                    execution_time_ms=(time.monotonic() - start) * 1000,
                )
        finally:
            cursor.close()

    def list_schemas(self) -> list[str]:
        result = self.execute("SHOW DATABASES")
        return [row[0] for row in result.rows]

    def list_tables(self, schema: Optional[str] = None) -> list[TableInfo]:
        if schema:
            result = self.execute(f"SHOW TABLES IN `{schema}`")
        else:
            result = self.execute("SHOW TABLES")

        tables = []
        for row in result.rows:
            tables.append(TableInfo(
                schema=schema or self.config.get("database", "default"),
                name=row[0],
                table_type="TABLE",
            ))
        return tables

    def describe_table(self, table: str, schema: Optional[str] = None) -> list[ColumnInfo]:
        qualified_name = f"`{schema}`.`{table}`" if schema else f"`{table}`"
        result = self.execute(f"DESCRIBE {qualified_name}")

        columns = []
        for row in result.rows:
            # Skip partition info separator rows
            if row[0] and not row[0].startswith("#") and row[0].strip():
                columns.append(ColumnInfo(
                    name=row[0],
                    data_type=row[1] if len(row) > 1 else "STRING",
                    nullable=True,  # Impala doesn't enforce NOT NULL
                    comment=row[2] if len(row) > 2 and row[2] else None,
                ))
        return columns

    def health_check(self) -> dict:
        try:
            start = time.monotonic()
            self.execute("SELECT 1")
            return {
                "status": "ok",
                "latency_ms": round((time.monotonic() - start) * 1000, 2),
            }
        except Exception as e:
            return {"status": "error", "details": str(e)}

    @staticmethod
    def _serialize_value(value: Any) -> Any:
        """Convert Impala types to JSON-serializable values."""
        if value is None:
            return None
        import datetime
        if isinstance(value, (datetime.datetime, datetime.date)):
            return value.isoformat()
        if isinstance(value, bytes):
            return value.decode("utf-8", errors="replace")
        return value
