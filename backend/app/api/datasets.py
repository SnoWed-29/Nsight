from pathlib import Path
from uuid import uuid4

from app.models import dataset
import polars as pl  # pyright: ignore[reportMissingImports]
from fastapi import APIRouter, File, HTTPException, UploadFile, Depends  # pyright: ignore[reportMissingImports]

from sqlalchemy.orm import Session # pyright: ignore[reportMissingImports]

from app.core.database import get_db
from app.models.dataset import Dataset
from app.services.query_engine import QueryEngine
from app.schemas.dataset import DatasetQueryRequest

from app.services.profiler import profile_dataset




router = APIRouter(prefix="/api/datasets", tags=["Datasets"])

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".csv", ".json", ".xlsx"}


def load_dataset(file_path: Path, extension: str) -> pl.DataFrame:
    if extension == ".csv":
        return pl.read_csv(file_path)

    if extension == ".json":
        return pl.read_json(file_path)

    if extension == ".xlsx":
        return pl.read_excel(file_path)

    raise ValueError(f"Unsupported file format: {extension}")


@router.post("/upload")
async def upload_dataset(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    ):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required",
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file format. "
                "Supported formats: CSV, JSON and XLSX."
            ),
        )

    dataset_id = str(uuid4())
    filename = f"{dataset_id}{extension}"
    file_path = UPLOAD_DIR / filename

    try:
        content = await file.read()
        file_path.write_bytes(content)

        df = load_dataset(file_path, extension)

    except Exception as exc:
        file_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=400,
            detail=f"Could not read dataset: {exc}",
        ) from exc

    profile = profile_dataset(df)

    dataset = Dataset(
        id=dataset_id,
        filename=file.filename,
        format=extension.removeprefix("."),
        file_path=str(file_path),
        rows=df.height,
        columns=df.width,
    )

    db.add(dataset)
    db.commit()
    db.refresh(dataset)

    return {
        "id": dataset_id,
        "filename": file.filename,
        "format": extension.removeprefix("."),
        "rows": dataset.rows,
        "columns": dataset.columns,
        "profile": profile
    }


@router.get("")
async def list_datasets(
        db: Session = Depends(get_db)
):
    datasets = (
        db.query(Dataset)
        .order_by(Dataset.created_at.desc())
        .all()
    )

    return datasets

@router.get("/{dataset_id}")
async def get_dataset(
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

    return dataset

@router.get("/{dataset_id}/preview")
async def preview_dataset(
    dataset_id: str,
    limit: int = 100,
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
        return QueryEngine.get_preview(
            file_path=dataset.file_path,
            file_format=dataset.format,
            limit=limit,
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
            detail=f"Could not preview dataset: {exc}",
        ) from exc

@router.post("/{dataset_id}/query")
async def query_dataset(
    dataset_id: str,
    request: DatasetQueryRequest,
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
        return QueryEngine.execute_query(
            file_path=dataset.file_path,
            file_format=dataset.format,
            sql=request.sql,
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
            detail=f"Query failed: {exc}",
        ) from exc