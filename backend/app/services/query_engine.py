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