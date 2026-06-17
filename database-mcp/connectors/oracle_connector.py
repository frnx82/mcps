"""Oracle Database Connector — uses oracledb (thin mode, no Oracle Client needed)."""

import time
import logging
from typing import Optional, Any

from connectors import BaseConnector, QueryResult, TableInfo, ColumnInfo

logger = logging.getLogger("mcp_database.oracle")


class OracleConnector(BaseConnector):
    """Connector for Oracle Database (on-prem).

    Uses python-oracledb in thin mode (pure Python, no Oracle Client installation needed).
    Supports connection pooling for production workloads.
    """

    def __init__(self, name: str, config: dict):
        super().__init__(name, "oracle", config)
        self._pool = None

    def connect(self) -> None:
        try:
            import oracledb

            dsn = self.config.get("dsn", "")
            if not dsn and self.config.get("host"):
                dsn = oracledb.makedsn(
                    self.config["host"],
                    self.config.get("port", 1521),
                    service_name=self.config.get("service_name", ""),
                )

            self._pool = oracledb.create_pool(
                user=self.config.get("user", ""),
                password=self.config.get("password", ""),
                dsn=dsn,
                min=self.config.get("min_pool_size", 1),
                max=self.config.get("max_pool_size", 5),
                increment=1,
            )
            self._connected = True
            logger.info("Oracle connection pool created: %s", self.name)
        except Exception as e:
            logger.error("Failed to connect to Oracle '%s': %s", self.name, e)
            self._connected = False
            raise

    def disconnect(self) -> None:
        if self._pool:
            try:
                self._pool.close(force=True)
            except Exception:
                pass
            self._pool = None
        self._connected = False
        logger.info("Oracle connection pool closed: %s", self.name)

    def execute(self, sql: str, params: Optional[dict] = None) -> QueryResult:
        start = time.monotonic()
        conn = self._pool.acquire()
        try:
            cursor = conn.cursor()
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
                    row_count=cursor.rowcount,
                    database=self.name,
                    query=sql,
                    execution_time_ms=(time.monotonic() - start) * 1000,
                )
        finally:
            self._pool.release(conn)

    def list_schemas(self) -> list[str]:
        result = self.execute(
            "SELECT username FROM all_users ORDER BY username"
        )
        return [row[0] for row in result.rows]

    def list_tables(self, schema: Optional[str] = None) -> list[TableInfo]:
        if schema:
            result = self.execute(
                "SELECT owner, table_name, 'TABLE' as table_type, num_rows "
                "FROM all_tables WHERE owner = :schema ORDER BY table_name",
                {"schema": schema.upper()},
            )
        else:
            result = self.execute(
                "SELECT owner, table_name, 'TABLE' as table_type, num_rows "
                "FROM user_tables ORDER BY table_name"
            )
        tables = []
        for row in result.rows:
            tables.append(TableInfo(
                schema=row[0],
                name=row[1],
                table_type=row[2],
                row_count=row[3],
            ))
        return tables

    def describe_table(self, table: str, schema: Optional[str] = None) -> list[ColumnInfo]:
        owner_clause = f"AND owner = :schema" if schema else ""
        params = {"table_name": table.upper()}
        if schema:
            params["schema"] = schema.upper()

        result = self.execute(
            f"SELECT column_name, data_type, nullable, data_default "
            f"FROM all_tab_columns "
            f"WHERE table_name = :table_name {owner_clause} "
            f"ORDER BY column_id",
            params,
        )

        # Get primary key columns
        pk_result = self.execute(
            f"SELECT cols.column_name FROM all_constraints cons "
            f"JOIN all_cons_columns cols ON cons.constraint_name = cols.constraint_name "
            f"AND cons.owner = cols.owner "
            f"WHERE cons.constraint_type = 'P' AND cols.table_name = :table_name "
            f"{'AND cons.owner = :schema' if schema else ''}",
            params,
        )
        pk_columns = {row[0] for row in pk_result.rows}

        columns = []
        for row in result.rows:
            columns.append(ColumnInfo(
                name=row[0],
                data_type=row[1],
                nullable=row[2] == "Y",
                is_primary_key=row[0] in pk_columns,
                default_value=row[3],
            ))
        return columns

    def health_check(self) -> dict:
        try:
            start = time.monotonic()
            self.execute("SELECT 1 FROM DUAL")
            return {
                "status": "ok",
                "latency_ms": round((time.monotonic() - start) * 1000, 2),
                "pool_busy": self._pool.busy if self._pool else 0,
                "pool_open": self._pool.opened if self._pool else 0,
            }
        except Exception as e:
            return {"status": "error", "details": str(e)}

    @staticmethod
    def _serialize_value(value: Any) -> Any:
        """Convert Oracle-specific types to JSON-serializable values."""
        if value is None:
            return None
        import datetime
        if isinstance(value, datetime.datetime):
            return value.isoformat()
        if isinstance(value, datetime.date):
            return value.isoformat()
        if isinstance(value, bytes):
            return value.hex()
        # Handle Oracle LOBs
        if hasattr(value, "read"):
            return value.read()
        return value
