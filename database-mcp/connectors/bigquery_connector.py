"""BigQuery Connector — uses google-cloud-bigquery."""

import time
import logging
from typing import Optional, Any

from connectors import BaseConnector, QueryResult, TableInfo, ColumnInfo

logger = logging.getLogger("mcp_database.bigquery")


class BigQueryConnector(BaseConnector):
    """Connector for Google BigQuery (GCP).

    Uses google-cloud-bigquery library.
    Supports service account credentials and workload identity.
    """

    def __init__(self, name: str, config: dict):
        super().__init__(name, "bigquery", config)
        self._client = None

    def connect(self) -> None:
        try:
            from google.cloud import bigquery

            project = self.config.get("project", "")
            creds_path = self.config.get("credentials_path", "")

            if creds_path:
                from google.oauth2 import service_account
                credentials = service_account.Credentials.from_service_account_file(creds_path)
                self._client = bigquery.Client(project=project, credentials=credentials)
            else:
                # Use default credentials (workload identity, ADC, etc.)
                self._client = bigquery.Client(project=project)

            self._connected = True
            logger.info("BigQuery connected: project=%s", project)
        except Exception as e:
            logger.error("Failed to connect to BigQuery '%s': %s", self.name, e)
            self._connected = False
            raise

    def disconnect(self) -> None:
        if self._client:
            try:
                self._client.close()
            except Exception:
                pass
            self._client = None
        self._connected = False
        logger.info("BigQuery client closed: %s", self.name)

    def execute(self, sql: str, params: Optional[dict] = None) -> QueryResult:
        from google.cloud import bigquery as bq

        start = time.monotonic()

        job_config = bq.QueryJobConfig()

        if params:
            query_params = []
            for key, value in params.items():
                if isinstance(value, int):
                    query_params.append(bq.ScalarQueryParameter(key, "INT64", value))
                elif isinstance(value, float):
                    query_params.append(bq.ScalarQueryParameter(key, "FLOAT64", value))
                else:
                    query_params.append(bq.ScalarQueryParameter(key, "STRING", str(value)))
            job_config.query_parameters = query_params

        query_job = self._client.query(sql, job_config=job_config)
        results = query_job.result()

        columns = [field.name for field in results.schema]
        rows = []
        for row in results:
            rows.append([self._serialize_value(row[col]) for col in columns])

        return QueryResult(
            columns=columns,
            rows=rows,
            row_count=len(rows),
            database=self.name,
            query=sql,
            execution_time_ms=(time.monotonic() - start) * 1000,
        )

    def list_schemas(self) -> list[str]:
        """List datasets in the project."""
        datasets = list(self._client.list_datasets())
        return [ds.dataset_id for ds in datasets]

    def list_tables(self, schema: Optional[str] = None) -> list[TableInfo]:
        """List tables in a dataset."""
        dataset = schema or self.config.get("dataset", "")
        if not dataset:
            # List tables across all datasets
            tables = []
            for ds in self._client.list_datasets():
                dataset_ref = self._client.dataset(ds.dataset_id)
                for table in self._client.list_tables(dataset_ref):
                    tables.append(TableInfo(
                        schema=ds.dataset_id,
                        name=table.table_id,
                        table_type=table.table_type,
                        row_count=None,
                    ))
            return tables
        else:
            dataset_ref = self._client.dataset(dataset)
            tables = []
            for table in self._client.list_tables(dataset_ref):
                tables.append(TableInfo(
                    schema=dataset,
                    name=table.table_id,
                    table_type=table.table_type,
                ))
            return tables

    def describe_table(self, table: str, schema: Optional[str] = None) -> list[ColumnInfo]:
        dataset = schema or self.config.get("dataset", "")
        table_ref = self._client.get_table(f"{dataset}.{table}")

        columns = []
        for field in table_ref.schema:
            columns.append(ColumnInfo(
                name=field.name,
                data_type=field.field_type,
                nullable=field.mode != "REQUIRED",
                comment=field.description,
            ))
        return columns

    def health_check(self) -> dict:
        try:
            start = time.monotonic()
            list(self._client.list_datasets(max_results=1))
            return {
                "status": "ok",
                "latency_ms": round((time.monotonic() - start) * 1000, 2),
                "project": self.config.get("project", ""),
            }
        except Exception as e:
            return {"status": "error", "details": str(e)}

    @staticmethod
    def _serialize_value(value: Any) -> Any:
        """Convert BigQuery types to JSON-serializable values."""
        if value is None:
            return None
        import datetime
        import decimal
        if isinstance(value, (datetime.datetime, datetime.date, datetime.time)):
            return value.isoformat()
        if isinstance(value, decimal.Decimal):
            return float(value)
        if isinstance(value, bytes):
            return value.hex()
        if isinstance(value, dict):
            return {k: BigQueryConnector._serialize_value(v) for k, v in value.items()}
        if isinstance(value, list):
            return [BigQueryConnector._serialize_value(v) for v in value]
        return value
