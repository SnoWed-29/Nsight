from fastapi import APIRouter, Depends, HTTPException # pyright: ignore[reportMissingImports]
from sqlalchemy.orm import Session # pyright: ignore[reportMissingImports]

from app.core.database import get_db
from app.models.dataset import Dataset
from app.schemas.chat import ChatRequest
from app.services.ai import AIService
from app.services.query_engine import QueryEngine
from app.services.sql_validator import validate_sql

router = APIRouter(
    prefix="/api/datasets",
    tags=["AI"],
)


@router.post("/{dataset_id}/chat")
async def chat_with_dataset(
    dataset_id: str,
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    dataset = (
        db.query(Dataset)
        .filter(Dataset.id == dataset_id)
        .first()
    )

    if not dataset:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found",
        )

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty",
        )

    try:
        schema = QueryEngine.get_schema(
            file_path=dataset.file_path,
            file_format=dataset.format,
        )

        ai_service = AIService()

        sql = ai_service.generate_sql(
            question=request.question,
            schema=schema,
        )

        validate_sql(sql)

        result = QueryEngine.execute_query(
            file_path=dataset.file_path,
            file_format=dataset.format,
            sql=sql,
        )

        answer = ai_service.explain_result(
            question=request.question,
            sql=sql,
            columns=result["columns"],
            rows=result["rows"],
        )

        return {
            "question": request.question,
            "sql": sql,
            "columns": result["columns"],
            "rows": result["rows"],
            "count": result["count"],
            "answer": answer,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"AI analysis failed: {exc}",
        ) from exc