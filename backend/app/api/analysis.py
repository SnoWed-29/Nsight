from fastapi import APIRouter, Depends, HTTPException # pyright: ignore[reportMissingImports]
from sqlalchemy.orm import Session # pyright: ignore[reportMissingImports]

from app.core.database import get_db
from app.models.dataset import Dataset
from app.services.insights import InsightEngine


router = APIRouter(
    prefix="/api/analysis",
    tags=["Analysis"],
)


@router.get("/{dataset_id}/insights")
async def get_insights(
    dataset_id: str,
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

    try:
        return InsightEngine.generate(
            file_path=dataset.file_path,
            file_format=dataset.format,
        )

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Analysis failed: {exc}",
        ) from exc