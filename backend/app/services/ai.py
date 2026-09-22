from typing import Any

from openai import OpenAI

from app.core.config import settings


class AIService:

    def __init__(self) -> None:
        self.client = OpenAI(
            api_key=settings.llm_api_key,
            base_url=settings.llm_base_url,
        )

    def generate_sql(
        self,
        question: str,
        schema: list[dict[str, Any]],
    ) -> str:

        schema_text = "\n".join(
            f'- {column["name"]}: {column["type"]}'
            for column in schema
        )

        prompt = f"""
You are the SQL generation engine for Nshight,
an AI data analysis application.

The user has uploaded a dataset exposed to DuckDB
as a table called `dataset`.

Dataset schema:

{schema_text}

User question:

{question}

Generate ONE DuckDB-compatible SQL SELECT statement
that answers the user's question.

Rules:

- Use only the `dataset` table.
- Generate exactly one SQL statement.
- Only SELECT statements are allowed.
- Do not modify data.
- Do not create tables or views.
- Do not use INSERT, UPDATE, DELETE, DROP, ALTER,
  CREATE, ATTACH, DETACH, COPY, EXPORT, IMPORT,
  INSTALL or LOAD.
- Use the exact column names from the schema.
- Return SQL only.
"""

        response = self.client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You generate safe read-only DuckDB SQL "
                        "for data analysis."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0,
        )

        content = response.choices[0].message.content

        if not content:
            raise ValueError(
                "The AI did not generate a SQL query."
            )

        return self.clean_sql(content)

    @staticmethod
    def clean_sql(sql: str) -> str:
        sql = sql.strip()

        if sql.startswith("```sql"):
            sql = sql[6:]

        elif sql.startswith("```"):
            sql = sql[3:]

        if sql.endswith("```"):
            sql = sql[:-3]

        return sql.strip()
    def explain_result(
    self,
    question: str,
    sql: str,
    columns: list[str],
    rows: list[list],
) -> str:

        result_text = "\n".join(
        str(row)
        for row in rows
        )

        prompt = f"""
            You are the data analyst for Nshight.

            Answer the user's question using ONLY the query result below.

            User question:
            {question}

            SQL used:
            {sql}

            Query result:
            {result_text}

            Rules:

            - Answer the user's question directly.
            - Use the actual values from the query result.
            - Treat the query result values as factual data.
            - Never use column names as if they were values.
            - Never invent values.
            - Never invent entities that are not present in the result.
            - If the result contains one row, explain that row directly.
            - If the result is empty, say that no matching data was found.
            - Keep the answer concise and natural.
            - Do not mention SQL, DuckDB, prompts, or internal implementation
            unless the user specifically asks about them.
            """

        response = self.client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a precise data analyst. "
                        "Only use information present in the query result."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0,
        )

        content = response.choices[0].message.content

        if not content:
            raise ValueError(
                "The AI did not generate an explanation."
            )

        return content.strip()