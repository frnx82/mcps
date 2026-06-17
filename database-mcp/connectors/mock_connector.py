"""Mock Database Connector — generates realistic sample data for testing."""

import time
import random
import logging
from typing import Optional, Any

from connectors import BaseConnector, QueryResult, TableInfo, ColumnInfo

logger = logging.getLogger("mcp_database.mock")

# ── Mock data templates ──────────────────────────────────────────────────────
MOCK_SCHEMAS = {
    "oracle": {
        "name": "Oracle (On-Prem)",
        "schemas": ["TRADING", "RISK", "REFERENCE", "AUDIT"],
        "tables": {
            "TRADING": [
                {"name": "TRADES", "type": "TABLE", "rows": 1500000,
                 "columns": [
                     {"name": "TRADE_ID", "type": "NUMBER(12)", "nullable": False, "pk": True},
                     {"name": "TRADE_DATE", "type": "DATE", "nullable": False, "pk": False},
                     {"name": "INSTRUMENT_ID", "type": "VARCHAR2(20)", "nullable": False, "pk": False},
                     {"name": "COUNTERPARTY_ID", "type": "NUMBER(8)", "nullable": False, "pk": False},
                     {"name": "QUANTITY", "type": "NUMBER(15,4)", "nullable": False, "pk": False},
                     {"name": "PRICE", "type": "NUMBER(18,6)", "nullable": False, "pk": False},
                     {"name": "CURRENCY", "type": "VARCHAR2(3)", "nullable": False, "pk": False},
                     {"name": "TRADE_STATUS", "type": "VARCHAR2(20)", "nullable": False, "pk": False},
                     {"name": "SETTLEMENT_DATE", "type": "DATE", "nullable": True, "pk": False},
                     {"name": "CREATED_AT", "type": "TIMESTAMP", "nullable": False, "pk": False},
                 ]},
                {"name": "ORDERS", "type": "TABLE", "rows": 3200000,
                 "columns": [
                     {"name": "ORDER_ID", "type": "NUMBER(12)", "nullable": False, "pk": True},
                     {"name": "ORDER_DATE", "type": "DATE", "nullable": False, "pk": False},
                     {"name": "INSTRUMENT_ID", "type": "VARCHAR2(20)", "nullable": False, "pk": False},
                     {"name": "SIDE", "type": "VARCHAR2(4)", "nullable": False, "pk": False},
                     {"name": "QUANTITY", "type": "NUMBER(15,4)", "nullable": False, "pk": False},
                     {"name": "LIMIT_PRICE", "type": "NUMBER(18,6)", "nullable": True, "pk": False},
                     {"name": "ORDER_STATUS", "type": "VARCHAR2(20)", "nullable": False, "pk": False},
                 ]},
                {"name": "POSITIONS", "type": "TABLE", "rows": 85000,
                 "columns": [
                     {"name": "POSITION_ID", "type": "NUMBER(12)", "nullable": False, "pk": True},
                     {"name": "ACCOUNT_ID", "type": "NUMBER(8)", "nullable": False, "pk": False},
                     {"name": "INSTRUMENT_ID", "type": "VARCHAR2(20)", "nullable": False, "pk": False},
                     {"name": "QUANTITY", "type": "NUMBER(15,4)", "nullable": False, "pk": False},
                     {"name": "MARKET_VALUE", "type": "NUMBER(18,4)", "nullable": True, "pk": False},
                     {"name": "AS_OF_DATE", "type": "DATE", "nullable": False, "pk": False},
                 ]},
            ],
            "RISK": [
                {"name": "VAR_DAILY", "type": "TABLE", "rows": 365000},
                {"name": "STRESS_RESULTS", "type": "TABLE", "rows": 52000},
                {"name": "LIMIT_BREACHES", "type": "TABLE", "rows": 1200},
            ],
            "REFERENCE": [
                {"name": "INSTRUMENTS", "type": "TABLE", "rows": 25000,
                 "columns": [
                     {"name": "INSTRUMENT_ID", "type": "VARCHAR2(20)", "nullable": False, "pk": True},
                     {"name": "INSTRUMENT_NAME", "type": "VARCHAR2(100)", "nullable": False, "pk": False},
                     {"name": "INSTRUMENT_TYPE", "type": "VARCHAR2(20)", "nullable": False, "pk": False},
                     {"name": "EXCHANGE", "type": "VARCHAR2(10)", "nullable": True, "pk": False},
                     {"name": "CURRENCY", "type": "VARCHAR2(3)", "nullable": False, "pk": False},
                     {"name": "ISIN", "type": "VARCHAR2(12)", "nullable": True, "pk": False},
                     {"name": "SEDOL", "type": "VARCHAR2(7)", "nullable": True, "pk": False},
                     {"name": "IS_ACTIVE", "type": "NUMBER(1)", "nullable": False, "pk": False},
                 ]},
                {"name": "COUNTERPARTIES", "type": "TABLE", "rows": 8500},
                {"name": "CURRENCIES", "type": "TABLE", "rows": 180},
                {"name": "EXCHANGES", "type": "TABLE", "rows": 60},
            ],
        },
    },
    "impala": {
        "name": "Impala (On-Prem)",
        "schemas": ["raw_data", "analytics", "staging"],
        "tables": {
            "raw_data": [
                {"name": "market_ticks", "type": "TABLE", "rows": 500000000},
                {"name": "order_book_snapshots", "type": "TABLE", "rows": 200000000},
                {"name": "transaction_log", "type": "TABLE", "rows": 150000000},
            ],
            "analytics": [
                {"name": "daily_pnl", "type": "TABLE", "rows": 1000000},
                {"name": "portfolio_summary", "type": "TABLE", "rows": 500000},
                {"name": "risk_metrics_agg", "type": "TABLE", "rows": 2000000},
            ],
        },
    },
    "bigquery": {
        "name": "BigQuery (GCP)",
        "schemas": ["reporting", "ml_features", "audit_logs"],
        "tables": {
            "reporting": [
                {"name": "trade_summary", "type": "TABLE", "rows": 10000000},
                {"name": "client_activity", "type": "TABLE", "rows": 5000000},
                {"name": "regulatory_reports", "type": "TABLE", "rows": 100000},
            ],
            "ml_features": [
                {"name": "price_features", "type": "TABLE", "rows": 50000000},
                {"name": "client_features", "type": "TABLE", "rows": 2000000},
            ],
        },
    },
    "cloudsql": {
        "name": "CloudSQL (GCP)",
        "schemas": ["app_data", "config", "user_mgmt"],
        "tables": {
            "app_data": [
                {"name": "alerts", "type": "TABLE", "rows": 50000,
                 "columns": [
                     {"name": "alert_id", "type": "SERIAL", "nullable": False, "pk": True},
                     {"name": "alert_type", "type": "VARCHAR(50)", "nullable": False, "pk": False},
                     {"name": "severity", "type": "VARCHAR(10)", "nullable": False, "pk": False},
                     {"name": "message", "type": "TEXT", "nullable": False, "pk": False},
                     {"name": "source_system", "type": "VARCHAR(50)", "nullable": False, "pk": False},
                     {"name": "created_at", "type": "TIMESTAMP", "nullable": False, "pk": False},
                     {"name": "acknowledged", "type": "BOOLEAN", "nullable": False, "pk": False},
                 ]},
                {"name": "dashboards", "type": "TABLE", "rows": 200},
                {"name": "scheduled_jobs", "type": "TABLE", "rows": 500},
            ],
            "config": [
                {"name": "system_params", "type": "TABLE", "rows": 150},
                {"name": "feature_flags", "type": "TABLE", "rows": 45},
            ],
        },
    },
}

# Sample data for generating mock query results
MOCK_TRADE_DATA = [
    [1001, "2026-06-17", "AAPL.US", 5001, 150.0, 192.45, "USD", "SETTLED", "2026-06-19", "2026-06-17T09:30:00"],
    [1002, "2026-06-17", "GOOGL.US", 5002, 25.0, 178.30, "USD", "CONFIRMED", "2026-06-19", "2026-06-17T09:31:00"],
    [1003, "2026-06-17", "DBK.DE", 5003, 500.0, 15.82, "EUR", "PENDING", None, "2026-06-17T10:15:00"],
    [1004, "2026-06-16", "7203.JP", 5001, 200.0, 2450.00, "JPY", "SETTLED", "2026-06-18", "2026-06-16T04:00:00"],
    [1005, "2026-06-16", "MSFT.US", 5004, 75.0, 445.20, "USD", "SETTLED", "2026-06-18", "2026-06-16T14:30:00"],
]


class MockConnector(BaseConnector):
    """Mock connector that returns realistic sample data.

    Use for development and testing without real database connections.
    """

    def __init__(self, name: str, db_type: str = "mock"):
        config = MOCK_SCHEMAS.get(name, MOCK_SCHEMAS.get("oracle", {}))
        super().__init__(name, db_type, config)
        self._mock_data = config

    def connect(self) -> None:
        self._connected = True
        logger.info("Mock connector '%s' connected (simulated)", self.name)

    def disconnect(self) -> None:
        self._connected = False

    def execute(self, sql: str, params: Optional[dict] = None) -> QueryResult:
        start = time.monotonic()
        # Simulate query latency
        time.sleep(random.uniform(0.01, 0.05))

        sql_upper = sql.upper().strip()

        # Return appropriate mock data based on query
        if "TRADES" in sql_upper or "TRADE" in sql_upper:
            columns = ["TRADE_ID", "TRADE_DATE", "INSTRUMENT_ID", "COUNTERPARTY_ID",
                       "QUANTITY", "PRICE", "CURRENCY", "TRADE_STATUS",
                       "SETTLEMENT_DATE", "CREATED_AT"]
            rows = MOCK_TRADE_DATA[:5]
        elif "SELECT 1" in sql_upper or "DUAL" in sql_upper:
            columns = ["RESULT"]
            rows = [[1]]
        elif "COUNT" in sql_upper:
            columns = ["COUNT"]
            rows = [[random.randint(1000, 5000000)]]
        elif "SUM" in sql_upper or "AVG" in sql_upper:
            columns = ["METRIC", "VALUE"]
            rows = [["total_volume", random.uniform(1000000, 50000000)],
                    ["avg_price", random.uniform(50, 500)]]
        else:
            columns = ["col_1", "col_2", "col_3"]
            rows = [[f"value_{i}", random.randint(1, 100), f"data_{i}"]
                    for i in range(min(10, random.randint(3, 15)))]

        return QueryResult(
            columns=columns,
            rows=rows,
            row_count=len(rows),
            database=self.name,
            query=sql,
            execution_time_ms=(time.monotonic() - start) * 1000,
        )

    def list_schemas(self) -> list[str]:
        return self._mock_data.get("schemas", [])

    def list_tables(self, schema: Optional[str] = None) -> list[TableInfo]:
        tables_data = self._mock_data.get("tables", {})
        if schema and schema in tables_data:
            tables_list = tables_data[schema]
        else:
            tables_list = []
            for s, tlist in tables_data.items():
                for t in tlist:
                    t["_schema"] = s
                    tables_list.append(t)

        tables = []
        for t in tables_list:
            tables.append(TableInfo(
                schema=t.get("_schema", schema or "default"),
                name=t["name"],
                table_type=t.get("type", "TABLE"),
                row_count=t.get("rows"),
            ))
        return tables

    def describe_table(self, table: str, schema: Optional[str] = None) -> list[ColumnInfo]:
        # Search for the table in mock data
        tables_data = self._mock_data.get("tables", {})
        for s, tlist in tables_data.items():
            for t in tlist:
                if t["name"].upper() == table.upper():
                    cols = t.get("columns", [])
                    if cols:
                        return [
                            ColumnInfo(
                                name=c["name"],
                                data_type=c["type"],
                                nullable=c.get("nullable", True),
                                is_primary_key=c.get("pk", False),
                            )
                            for c in cols
                        ]

        # Fallback: generic columns
        return [
            ColumnInfo(name="id", data_type="INTEGER", nullable=False, is_primary_key=True),
            ColumnInfo(name="name", data_type="VARCHAR(100)", nullable=False),
            ColumnInfo(name="value", data_type="DECIMAL(18,4)", nullable=True),
            ColumnInfo(name="created_at", data_type="TIMESTAMP", nullable=False),
        ]

    def health_check(self) -> dict:
        return {"status": "ok", "latency_ms": 1.0, "mode": "mock"}

    def get_info(self) -> dict:
        info = super().get_info()
        info["display_name"] = self._mock_data.get("name", self.name)
        info["mode"] = "mock"
        return info
