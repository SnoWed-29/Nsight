import re


FORBIDDEN_KEYWORDS = {
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


def validate_sql(sql: str) -> None:
    normalized = sql.strip().upper()

    if not normalized:
        raise ValueError("SQL query cannot be empty.")

    if not normalized.startswith("SELECT"):
        raise ValueError(
            "Only SELECT queries are allowed."
        )

    statements = [
        statement.strip()
        for statement in sql.split(";")
        if statement.strip()
    ]

    if len(statements) != 1:
        raise ValueError(
            "Only one SQL statement is allowed."
        )

    for keyword in FORBIDDEN_KEYWORDS:
        pattern = rf"\b{re.escape(keyword)}\b"

        if re.search(pattern, normalized):
            raise ValueError(
                f"Forbidden SQL keyword: {keyword}"
            )