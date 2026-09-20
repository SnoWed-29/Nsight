from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text # pyright: ignore[reportMissingImports]
from sqlalchemy.orm import Mapped, mapped_column   # pyright: ignore[reportMissingImports]

from app.core.database import Base


class Dataset(Base):
    __tablename__ = "datasets"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    format: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    file_path: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    rows: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    columns: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )