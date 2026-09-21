from pathlib import Path
from typing import Any

import duckdb # pyright: ignore[reportMissingImports]
import polars as pl # pyright: ignore[reportMissingImports]


class InsightEngine:

    @staticmethod
    def generate(
        file_path: str,
        file_format: str,
    ) -> dict[str, Any]:

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError("Dataset file not found")

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

            total_rows = connection.execute(
                "SELECT COUNT(*) FROM dataset"
            ).fetchone()[0]

            total_columns = len(
                connection.execute(
                    "DESCRIBE dataset"
                ).fetchall()
            )

            # ADD IT HERE
            numeric_insights = InsightEngine.numeric_insights(
                connection
            )

            quality_insights = InsightEngine.data_quality_insights(
                connection
            )

            categorical_insights = InsightEngine.categorical_insights(
                connection
            )

            insights = (
                numeric_insights
                + quality_insights
                + categorical_insights
            )

            return {
                "dataset": {
                    "rows": total_rows,
                    "columns": total_columns,
                },
                "insights": insights,
            }

        finally:
            connection.close()

    @staticmethod
    def numeric_insights(
        connection: duckdb.DuckDBPyConnection,
    ) -> list[dict[str, Any]]:

        insights = []

        columns = connection.execute(
            "DESCRIBE dataset"
        ).fetchall()

        numeric_types = {
            "INTEGER",
            "BIGINT",
            "DOUBLE",
            "FLOAT",
            "DECIMAL",
            "HUGEINT",
            "SMALLINT",
            "TINYINT",
        }

        for column in columns:
            column_name = column[0]
            column_type = column[1].upper()

            if not any(
                numeric_type in column_type
                for numeric_type in numeric_types
            ):
                continue

            result = connection.execute(
                f"""
                SELECT
                    MIN("{column_name}") AS minimum,
                    MAX("{column_name}") AS maximum,
                    AVG("{column_name}") AS average
                FROM dataset
                """
            ).fetchone()

            if result:
                minimum, maximum, average = result

                insights.append({
                    "type": "numeric_summary",
                    "column": column_name,
                    "minimum": minimum,
                    "maximum": maximum,
                    "average": average,
                })

        return insights
    @staticmethod
    def data_quality_insights(
        connection: duckdb.DuckDBPyConnection,
    ) -> list[dict[str, Any]]:

        insights = []

        columns = connection.execute(
            "DESCRIBE dataset"
        ).fetchall()

        for column in columns:
            column_name = column[0]

            result = connection.execute(
                f"""
                SELECT COUNT(*)
                FROM dataset
                WHERE "{column_name}" IS NULL
                """
            ).fetchone()

            null_count = result[0]

            if null_count > 0:
                insights.append({
                    "type": "missing_values",
                    "column": column_name,
                    "count": null_count,
                })

        duplicate_count = connection.execute(
            """
            SELECT COUNT(*)
            FROM (
                SELECT *
                FROM dataset
                GROUP BY ALL
                HAVING COUNT(*) > 1
            )
            """
        ).fetchone()[0]

        if duplicate_count > 0:
            insights.append({
                "type": "duplicate_rows",
                "count": duplicate_count,
            })

        return insights
    @staticmethod
    def categorical_insights(
        connection: duckdb.DuckDBPyConnection,
    ) -> list[dict[str, Any]]:

        insights = []

        columns = connection.execute(
            "DESCRIBE dataset"
        ).fetchall()

        categorical_types = {
            "VARCHAR",
            "TEXT",
        }

        total_rows = connection.execute(
            "SELECT COUNT(*) FROM dataset"
        ).fetchone()[0]

        if total_rows == 0:
            return insights

        for column in columns:
            column_name = column[0]
            column_type = column[1].upper()

            if not any(
                data_type in column_type
                for data_type in categorical_types
            ):
                continue

            unique_count = connection.execute(
                f"""
                SELECT COUNT(DISTINCT "{column_name}")
                FROM dataset
                """
            ).fetchone()[0]

            # Avoid analyzing columns with too many unique values.
            if unique_count == 0 or unique_count > 50:
                continue

            result = connection.execute(
                f"""
                SELECT
                    "{column_name}" AS value,
                    COUNT(*) AS count
                FROM dataset
                WHERE "{column_name}" IS NOT NULL
                GROUP BY "{column_name}"
                ORDER BY count DESC
                LIMIT 5
                """
            ).fetchall()

            values = []

            for value, count in result:
                percentage = round(
                    (count / total_rows) * 100,
                    2,
                )

                values.append({
                    "value": value,
                    "count": count,
                    "percentage": percentage,
                })

            if values:
                insights.append({
                    "type": "categorical_distribution",
                    "column": column_name,
                    "unique_values": unique_count,
                    "top_values": values,
                })

        return insights