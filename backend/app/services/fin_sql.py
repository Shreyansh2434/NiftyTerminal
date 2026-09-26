"""Safe, read-only SQL helpers used by the copilot.

The copilot is deliberately unable to mutate the application's database.  This
module keeps the policy in one small, dependency-free place so it can also be
used by CLI and notebook callers.
"""
from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any


class ReadOnlySQLError(ValueError):
    """Raised when a query is not an unambiguous single read-only statement."""


class FinSQLGenerator:
    """Conservative natural-language-to-SQL translator for known research phrases."""

    def generate(self, prompt: str) -> dict[str, Any]:
        text = prompt.strip().lower()
        if not text:
            raise ReadOnlySQLError("Financial query must not be empty")
        if any(token in text for token in ("drop ", "insert ", "update ", "delete ", "alter ")):
            raise ReadOnlySQLError("Mutating financial queries are not allowed")
        if "nifty" in text and "vix" in text and ("fell" in text or "fall" in text):
            sql = (
                "SELECT timestamp, symbol, close_return_pct, vix_return_pct "
                "FROM market_regimes WHERE symbol = :symbol "
                "AND close_return_pct <= :price_threshold "
                "AND vix_return_pct >= :vix_threshold ORDER BY timestamp DESC"
            )
            return {"sql": validate_read_only_sql(sql), "parameters": {"symbol": "NIFTY", "price_threshold": -2.0, "vix_threshold": 10.0}, "confidence": 0.92, "sample_size_estimate": 0}
        raise ReadOnlySQLError("Unsupported query pattern; use a supported read-only market-regime question")


fin_sql = FinSQLGenerator()


_MUTATING = re.compile(
    r"\b(?:insert|update|delete|merge|replace|upsert|alter|drop|create|truncate|"
    r"grant|revoke|attach|detach|vacuum|reindex|analyze|pragma|copy|call|do)\b",
    re.IGNORECASE,
)
_COMMENT = re.compile(r"--|/\*|\*/")


def _without_literals(sql: str) -> str:
    """Remove quoted strings/identifiers while retaining statement structure."""
    return re.sub(r"'(?:''|[^'])*'|\"(?:\"\"|[^\"])*\"|`(?:``|[^`])*`", "''", sql)


def validate_read_only_sql(sql: str) -> str:
    """Validate and return *sql* as a single SELECT/WITH statement."""
    if not isinstance(sql, str) or not sql.strip():
        raise ReadOnlySQLError("SQL query must not be empty")
    if len(sql) > 20_000:
        raise ReadOnlySQLError("SQL query is too long")
    if _COMMENT.search(sql):
        raise ReadOnlySQLError("SQL comments are not allowed")
    masked = _without_literals(sql).strip()
    statements = [part.strip() for part in masked.split(";") if part.strip()]
    if len(statements) != 1:
        raise ReadOnlySQLError("Only one SQL statement is allowed")
    statement = statements[0]
    if not re.match(r"^(?:select|with)\b", statement, re.IGNORECASE):
        raise ReadOnlySQLError("Only SELECT or WITH queries are allowed")
    if _MUTATING.search(statement):
        raise ReadOnlySQLError("Mutating or administrative SQL is not allowed")
    return sql.strip().rstrip(";").strip()


# Short alias useful to callers and backwards-compatible with early prototypes.
validate_sql = validate_read_only_sql


def execute_read_only(
    connection: Any,
    sql: str,
    parameters: Mapping[str, Any] | Sequence[Any] | None = None,
) -> list[dict[str, Any]]:
    """Execute a validated query against a DB-API or SQLAlchemy connection."""
    query = validate_read_only_sql(sql)
    if connection.__class__.__module__.startswith("sqlalchemy"):
        from sqlalchemy import text
        result = connection.execute(text(query), parameters or {})
    else:
        result = connection.execute(query, parameters or {})
    if hasattr(result, "mappings"):
        return [dict(row) for row in result.mappings().all()]
    rows = result.fetchall()
    columns = [item[0] for item in (result.description or [])]
    return [dict(zip(columns, row)) for row in rows]


__all__ = ["ReadOnlySQLError", "execute_read_only", "validate_read_only_sql", "validate_sql"]
