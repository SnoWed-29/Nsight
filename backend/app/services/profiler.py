from typing import Any

import polars as pl  # pyright: ignore[reportMissingImports]

def profile_dataset(df: pl.DataFrame) -> dict[str, Any]:
    columns = []

    for column in df.columns:
        series = df[column]
        column_info = {
            "name": column,
            "dtype": str(series.dtype),
            "nullable": series.null_count() > 0,
            "null_count": series.null_count(),
            "null_percentage": round(
                (series.null_count() / df.height) * 100,
                2,
            )
            if df.height > 0
            else 0,
            "unique_count": series.n_unique(),
        }

        if series.dtype.is_numeric():
            column_info["statistics"] = {
                "min": series.min(),
                "max": series.max(),
                "mean": series.mean(),
                "median": series.median(),
            }

        columns.append(column_info)
    duplicate_count = df.height - df.unique().height

    return  {
        "rows": df.height,
        "columns": df.width,
        "duplicated_rows": duplicate_count,
        "columns_info": columns,
    }