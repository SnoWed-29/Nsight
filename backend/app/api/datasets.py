from pathlib import Path
from uuid import uuid4

import polars as pl  # pyright: ignore[reportMissingImports]
from fastapi import APIRouter, File, HTTPException, UploadFile  # pyright: ignore[reportMissingImports]

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
async def upload_dataset(file: UploadFile = File(...)):
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

    return {
        "id": dataset_id,
        "filename": file.filename,
        "format": extension.removeprefix("."),
        "profile": profile
    }