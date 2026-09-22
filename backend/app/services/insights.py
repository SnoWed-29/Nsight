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
            
            outlier_insights = InsightEngine.outlier_insights(
                connection
            )
            trend_insights = InsightEngine.trend_insights(
                connection
            )
            raw_insights = (
                numeric_insights
                + quality_insights
                + categorical_insights
                + outlier_insights
                + trend_insights
            )

            insights = [
                InsightEngine.normalize_insight(insight)
                for insight in raw_insights
            ]

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
    @staticmethod
    def outlier_insights(
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
                    quantile_cont("{column_name}", 0.25),
                    quantile_cont("{column_name}", 0.75)
                FROM dataset
                WHERE "{column_name}" IS NOT NULL
                """
            ).fetchone()

            if not result:
                continue

            q1, q3 = result

            if q1 is None or q3 is None:
                continue

            iqr = q3 - q1

            lower_bound = q1 - (1.5 * iqr)
            upper_bound = q3 + (1.5 * iqr)

            outlier_count = connection.execute(
                f"""
                SELECT COUNT(*)
                FROM dataset
                WHERE "{column_name}" < ?
                   OR "{column_name}" > ?
                """,
                [lower_bound, upper_bound],
            ).fetchone()[0]

            if outlier_count == 0:
                continue

            outliers = connection.execute(
                f"""
                SELECT "{column_name}"
                FROM dataset
                WHERE "{column_name}" < ?
                   OR "{column_name}" > ?
                ORDER BY "{column_name}" DESC
                LIMIT 10
                """,
                [lower_bound, upper_bound],
            ).fetchall()

            values = [
                row[0]
                for row in outliers
            ]

            insights.append({
                "type": "outliers",
                "column": column_name,
                "count": outlier_count,
                "lower_bound": lower_bound,
                "upper_bound": upper_bound,
                "values": values,
            })

        return insights
    @staticmethod
    def trend_insights(
        connection: duckdb.DuckDBPyConnection,
    ) -> list[dict[str, Any]]:

        insights = []

        columns = connection.execute(
            "DESCRIBE dataset"
        ).fetchall()

        column_names = {
            column[0].lower(): column[0]
            for column in columns
        }

        date_column = None

        for name in ["date", "datetime", "timestamp", "created_at"]:
            if name in column_names:
                date_column = column_names[name]
                break

        if not date_column:
            return insights

        numeric_columns = []

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

            if any(
                numeric_type in column_type
                for numeric_type in numeric_types
            ):
                numeric_columns.append(column_name)

        for numeric_column in numeric_columns:
            result = connection.execute(
                f"""
                SELECT
                    DATE_TRUNC(
                        'month',
                        CAST("{date_column}" AS DATE)
                    ) AS month,
                    SUM("{numeric_column}") AS total,
                    AVG("{numeric_column}") AS average
                FROM dataset
                WHERE "{date_column}" IS NOT NULL
                GROUP BY month
                ORDER BY month
                """
            ).fetchall()

            if len(result) < 2:
                continue

            periods = []

            for index, row in enumerate(result):
                month, total, average = row

                change_percentage = None

                if index > 0:
                    previous_total = result[index - 1][1]

                    if previous_total:
                        change_percentage = round(
                            (
                                (total - previous_total)
                                / previous_total
                            ) * 100,
                            2,
                        )

                periods.append({
                    "month": str(month),
                    "total": total,
                    "average": average,
                    "change_percentage": change_percentage,
                })

            insights.append({
                "type": "time_series",
                "column": numeric_column,
                "period": "month",
                "values": periods,
            })

        return insights
    @staticmethod
    def normalize_insight(
        insight: dict[str, Any],
    ) -> dict[str, Any]:

        insight_type = insight["type"]

        titles = {
            "numeric_summary": "Numeric summary",
            "missing_values": "Missing values detected",
            "duplicate_rows": "Duplicate rows detected",
            "categorical_distribution": "Categorical distribution",
            "outliers": "Potential outliers detected",
            "time_series": "Time series trend",
        }

        descriptions = {
            "numeric_summary": (
                "Summary statistics for a numeric column."
            ),
            "missing_values": (
                "This column contains missing values."
            ),
            "duplicate_rows": (
                "The dataset contains duplicate rows."
            ),
            "categorical_distribution": (
                "Distribution of the most common values."
            ),
            "outliers": (
                "Some values are statistically unusual based on the IQR method."
            ),
            "time_series": (
                "Monthly changes and aggregated values over time."
            ),
        }

        severity = "info"

        if insight_type == "missing_values":
            severity = "warning"

        elif insight_type == "duplicate_rows":
            severity = "warning"

        elif insight_type == "outliers":
            severity = "notice"

        return {
            "type": insight_type,
            "severity": severity,
            "title": titles.get(
                insight_type,
                "Dataset insight",
            ),
            "description": descriptions.get(
                insight_type,
                "An insight was detected in the dataset.",
            ),
            "data": insight,
        }