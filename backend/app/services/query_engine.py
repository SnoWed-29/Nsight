from locale import normalize
from pathlib import Path

import duckdb # pyright: ignore[reportMissingImports]
import polars as pl # pyright: ignore[reportMissingImports]


class QueryEngine:
    @staticmethod
    def get_preview(
        file_path: str,
        file_format: str,
        limit: int = 100,
    ) -> dict:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError("Database file not found")

        if limit < 1 or limit > 1000:
            raise ValueError("limit must be between 1 and 1000")

        connection = duckdb.connect()

        try:
            if file_format == "csv":
                query = """
                    SELECT *
                    FROM read_csv_auto(?)
                    LIMIT ?
                """

                result = connection.execute(
                    query,
                    [str(path), limit],
                ).pl()

            elif file_format == "xlsx":
                dataframe = pl.read_excel(path)

                result = (
                    connection
                    .from_arrow(dataframe.to_arrow())
                    .limit(limit)
                    .pl()
                )
            else:
                raise ValueError(
                    f"Unsupported dataset format: {file_format}"
                )

            return {
                "columns": result.columns,
                "rows": result.to_dicts(),
                "count": result.height,
            }
        finally:
            connection.close()

    @staticmethod
    def execute_query(
        file_path: str,
        file_format: str,
        sql: str,
    ) -> dict:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError("Dataset file not found")

        sql = sql.strip()

        if not sql:
            raise ValueError("SQL query cannot be empty")

        forbidden_keywords = {
            "INSERT",
            "UPDATE",
            "DELETE",
            "DROP",
            "ALTER",
            "CREATE",
            "TRUNCATE",
            "ATTACH",
            "DETACH",
            "COPY",
            "EXPORT",
            "IMPORT",
            "INSTALL",
            "LOAD",
        }

        normalized_sql = sql.upper()

        for keyword in forbidden_keywords:
            if keyword in normalized_sql:
                raise ValueError(
                    f"SQL operation '{keyword}' is not allowed"
                )

        connection = duckdb.connect()

        try:
            escaped_path = str(path).replace("'", "''")

            if file_format == "csv":
                connection.execute(
                    f"""
                    CREATE VIEW dataset AS
                    SELECT *
                    FROM read_csv_auto('{escaped_path}')
                    """
                )

            elif file_format == "json":
                connection.execute(
                    f"""
                    CREATE VIEW dataset AS
                    SELECT *
                    FROM read_json_auto('{escaped_path}')
                    """
                )

            elif file_format == "xlsx":
                dataframe = pl.read_excel(path)

                connection.register(
                    "dataset",
                    dataframe.to_arrow(),
                )

            else:
                raise ValueError(
                    f"Unsupported dataset format: {file_format}"
                )

            result = connection.execute(sql).pl()

            return {
                "columns": result.columns,
                "rows": result.to_dicts(),
                "count": result.height,
            }

        finally:
            connection.close()