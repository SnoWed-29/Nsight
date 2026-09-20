from datetime import datetime

from pydantic import BaseModel # pyright: ignore[reportMissingImports]


class DatasetResponse(BaseModel):
    id: str
    filename: str
    format: str
    rows: int
    columns: int
    file_path: str
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }