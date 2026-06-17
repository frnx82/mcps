"""Abstract base connector — defines the interface all database connectors must implement."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class QueryResult:
    """Result of a database query."""
    columns: list[str]
    rows: list[list[Any]]
    row_count: int
    database: str
    query: str
    execution_time_ms: float = 0.0
    truncated: bool = False  # True if rows were limited

    def to_dict(self) -> dict:
        return {
            "columns": self.columns,
            "rows": self.rows,
            "row_count": self.row_count,
            "database": self.database,
            "execution_time_ms": round(self.execution_time_ms, 2),
            "truncated": self.truncated,
        }


@dataclass
class TableInfo:
    """Metadata for a database table."""
    schema: str
    name: str
    table_type: str = "TABLE"  # TABLE, VIEW, MATERIALIZED VIEW
    row_count: Optional[int] = None
    comment: Optional[str] = None

    def to_dict(self) -> dict:
        result = {
            "schema": self.schema,
            "name": self.name,
            "type": self.table_type,
        }
        if self.row_count is not None:
            result["row_count"] = self.row_count
        if self.comment:
            result["comment"] = self.comment
        return result


@dataclass
class ColumnInfo:
    """Metadata for a table column."""
    name: str
    data_type: str
    nullable: bool = True
    is_primary_key: bool = False
    default_value: Optional[str] = None
    comment: Optional[str] = None

    def to_dict(self) -> dict:
        result = {
            "name": self.name,
            "type": self.data_type,
            "nullable": self.nullable,
            "is_primary_key": self.is_primary_key,
        }
        if self.default_value is not None:
            result["default"] = self.default_value
        if self.comment:
            result["comment"] = self.comment
        return result


class BaseConnector(ABC):
    """Abstract base class for all database connectors.

    Each connector must implement these methods to provide a unified
    interface regardless of the underlying database technology.
    """

    def __init__(self, name: str, db_type: str, config: dict):
        self.name = name
        self.db_type = db_type
        self.config = config
        self._connected = False

    @abstractmethod
    def connect(self) -> None:
        """Establish connection to the database."""
        ...

    @abstractmethod
    def disconnect(self) -> None:
        """Close the database connection and release resources."""
        ...

    @abstractmethod
    def execute(self, sql: str, params: Optional[dict] = None) -> QueryResult:
        """Execute a SQL query and return results.

        Args:
            sql: SQL query string.
            params: Optional query parameters for parameterized queries.

        Returns:
            QueryResult with columns, rows, and metadata.
        """
        ...

    @abstractmethod
    def list_schemas(self) -> list[str]:
        """List all available schemas/databases."""
        ...

    @abstractmethod
    def list_tables(self, schema: Optional[str] = None) -> list[TableInfo]:
        """List tables in a schema.

        Args:
            schema: Schema name. If None, list tables in the default schema.

        Returns:
            List of TableInfo objects.
        """
        ...

    @abstractmethod
    def describe_table(self, table: str, schema: Optional[str] = None) -> list[ColumnInfo]:
        """Get column details for a table.

        Args:
            table: Table name.
            schema: Schema name. If None, use the default schema.

        Returns:
            List of ColumnInfo objects.
        """
        ...

    @abstractmethod
    def health_check(self) -> dict:
        """Check connection health.

        Returns:
            Dict with keys: status (ok|error), latency_ms, details
        """
        ...

    @property
    def is_connected(self) -> bool:
        return self._connected

    def get_info(self) -> dict:
        """Return basic info about this connector."""
        return {
            "name": self.name,
            "type": self.db_type,
            "connected": self._connected,
        }
