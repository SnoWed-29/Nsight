import re


FORBIDDEN_KEYWORDS = {
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "ATTACH",
    "DETACH",
    "COPY",
    "EXPORT",
    "IMPORT",
    "INSTALL",
    "LOAD",
}


def validate_sql(sql: str) -> None:
    sql = sql.strip()

    if not sql:
        raise ValueError("SQL query cannot be empty.")

    # Remove one optional trailing semicolon.
    normalized_sql = sql.rstrip(";").strip()

    # Only one statement is allowed.
    if ";" in normalized_sql:
        raise ValueError(
            "Only one SQL statement is allowed."
        )

    # Only SELECT queries are currently supported.
    if not re.match(
        r"^SELECT\b",
        normalized_sql,
        re.IGNORECASE,
    ):
        raise ValueError(
            "Only SELECT queries are allowed."
        )

    # Reject dangerous SQL keywords.
    for keyword in FORBIDDEN_KEYWORDS:
        pattern = rf"\b{re.escape(keyword)}\b"

        if re.search(
            pattern,
            normalized_sql,
            re.IGNORECASE,
        ):
            raise ValueError(
                f"Forbidden SQL keyword: {keyword}"
            )
        
def validate_dataset_reference(sql: str) -> None:
    references = re.findall(
        r"\b(?:FROM|JOIN)\s+([a-zA-Z_][a-zA-Z0-9_]*)",
        sql,
        re.IGNORECASE,
    )

    for table in references:
        if table.lower() != "dataset":
            raise ValueError(
                f"Only the dataset table can be queried: {table}"
            )