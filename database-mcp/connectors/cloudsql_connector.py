"""CloudSQL Connector — supports both PostgreSQL (pg8000) and MySQL (PyMySQL)."""

import time
import logging
from typing import Optional, Any

from connectors import BaseConnector, QueryResult, TableInfo, ColumnInfo

logger = logging.getLogger("mcp_database.cloudsql")


class CloudSQLConnector(BaseConnector):
    """Connector for Google Cloud SQL (PostgreSQL or MySQL).

    Connects via Cloud SQL Auth Proxy sidecar (recommended for GDC) or direct IP.
    Auto-detects PostgreSQL vs MySQL from config.
    """

    def __init__(self, name: str, db_type: str, config: dict):
        super().__init__(name, db_type, config)
        self._conn = None
        self._is_postgres = db_type == "cloudsql_pg"

    def connect(self) -> None:
        try:
            if self._is_postgres:
                self._connect_postgres()
            else:
                self._connect_mysql()
            self._connected = True
            logger.info("CloudSQL (%s) connected: %s",
                        "PostgreSQL" if self._is_postgres else "MySQL", self.name)
        except Exception as e:
            logger.error("Failed to connect to CloudSQL '%s': %s", self.name, e)
            self._connected = False
            raise

    def _connect_postgres(self) -> None:
        import pg8000

        self._conn = pg8000.connect(
            host=self.config.get("host", "127.0.0.1"),
            port=int(self.config.get("port", 5432)),
            user=self.config.get("user", ""),
            password=self.config.get("password", ""),
            database=self.config.get("database", ""),
        )
        self._conn.autocommit = True

    def _connect_mysql(self) -> None:
        import pymysql

        self._conn = pymysql.connect(
            host=self.config.get("host", "127.0.0.1"),
            port=int(self.config.get("port", 3306)),
            user=self.config.get("user", ""),
            password=self.config.get("password", ""),
            database=self.config.get("database", ""),
            autocommit=True,
            charset="utf8mb4",
        )

    def disconnect(self) -> None:
        if self._conn:
            try:
                self._conn.close()
            except Exception:
                pass
            self._conn = None
        self._connected = False
        logger.info("CloudSQL connection closed: %s", self.name)

    def execute(self, sql: str, params: Optional[dict] = None) -> QueryResult:
        start = time.monotonic()
        cursor = self._conn.cursor()
        try:
            if params:
                cursor.execute(sql, params)
            else:
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
                    row_count=cursor.rowcount if cursor.rowcount >= 0 else 0,
                    database=self.name,
                    query=sql,
                    execution_time_ms=(time.monotonic() - start) * 1000,
                )
        finally:
            cursor.close()

    def list_schemas(self) -> list[str]:
        if self._is_postgres:
            result = self.execute(
                "SELECT schema_name FROM information_schema.schemata "
                "WHERE schema_name NOT IN ('pg_catalog', 'information_schema', 'pg_toast') "
                "ORDER BY schema_name"
            )
        else:
            result = self.execute("SHOW DATABASES")
        return [row[0] for row in result.rows]

    def list_tables(self, schema: Optional[str] = None) -> list[TableInfo]:
        if self._is_postgres:
            schema = schema or "public"
            result = self.execute(
                "SELECT table_schema, table_name, table_type "
                "FROM information_schema.tables "
                "WHERE table_schema = %s ORDER BY table_name",
                (schema,),
            )
        else:
            if schema:
                result = self.execute(f"SHOW TABLES FROM `{schema}`")
            else:
                result = self.execute("SHOW TABLES")

        tables = []
        if self._is_postgres:
            for row in result.rows:
                tables.append(TableInfo(
                    schema=row[0],
                    name=row[1],
                    table_type=row[2],
                ))
        else:
            for row in result.rows:
                tables.append(TableInfo(
                    schema=schema or self.config.get("database", ""),
                    name=row[0],
                    table_type="TABLE",
                ))
        return tables

    def describe_table(self, table: str, schema: Optional[str] = None) -> list[ColumnInfo]:
        if self._is_postgres:
            schema = schema or "public"
            result = self.execute(
                "SELECT c.column_name, c.data_type, c.is_nullable, c.column_default, "
                "CASE WHEN tc.constraint_type = 'PRIMARY KEY' THEN true ELSE false END as is_pk "
                "FROM information_schema.columns c "
                "LEFT JOIN information_schema.key_column_usage kcu "
                "  ON c.table_schema = kcu.table_schema "
                "  AND c.table_name = kcu.table_name "
                "  AND c.column_name = kcu.column_name "
                "LEFT JOIN information_schema.table_constraints tc "
                "  ON kcu.constraint_name = tc.constraint_name "
                "  AND tc.constraint_type = 'PRIMARY KEY' "
                "WHERE c.table_schema = %s AND c.table_name = %s "
                "ORDER BY c.ordinal_position",
                (schema, table),
            )
        else:
            result = self.execute(f"DESCRIBE `{table}`")

        columns = []
        if self._is_postgres:
            for row in result.rows:
                columns.append(ColumnInfo(
                    name=row[0],
                    data_type=row[1],
                    nullable=row[2] == "YES",
                    default_value=row[3],
                    is_primary_key=bool(row[4]),
                ))
        else:
            for row in result.rows:
                columns.append(ColumnInfo(
                    name=row[0],
                    data_type=row[1],
                    nullable="YES" in str(row[2]).upper() if len(row) > 2 else True,
                    default_value=row[4] if len(row) > 4 else None,
                    is_primary_key="PRI" in str(row[3]).upper() if len(row) > 3 else False,
                ))
        return columns

    def health_check(self) -> dict:
        try:
            start = time.monotonic()
            self.execute("SELECT 1")
            return {
                "status": "ok",
                "latency_ms": round((time.monotonic() - start) * 1000, 2),
                "engine": "PostgreSQL" if self._is_postgres else "MySQL",
            }
        except Exception as e:
            return {"status": "error", "details": str(e)}

    @staticmethod
    def _serialize_value(value: Any) -> Any:
        """Convert database types to JSON-serializable values."""
        if value is None:
            return None
        import datetime
        import decimal
        if isinstance(value, (datetime.datetime, datetime.date, datetime.time)):
            return value.isoformat()
        if isinstance(value, decimal.Decimal):
            return float(value)
        if isinstance(value, bytes):
            return value.decode("utf-8", errors="replace")
        if isinstance(value, memoryview):
            return bytes(value).decode("utf-8", errors="replace")
        return value
