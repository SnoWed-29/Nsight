from pathlib import Path

from sqlalchemy import create_engine # pyright: ignore[reportMissingImports]
from sqlalchemy.orm import DeclarativeBase, sessionmaker # pyright: ignore[reportMissingImports]

DATABASE_DIR = Path("data")
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_URL = f"sqlite:///{DATABASE_DIR / 'nshight.db'}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    bind = engine,
    autoflush=False,
    autocommit=False
)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()