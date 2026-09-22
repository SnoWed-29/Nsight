from fastapi import FastAPI  # pyright: ignore[reportMissingImports]

from app.api.datasets import router as datasets_router
from app.core.database import Base, engine
from app.models.dataset import Dataset
from app.api.analysis import router as analysis_router
from app.api.chat import router as chat_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Nsight API",
    version = "0.1.0"
)


app.include_router(datasets_router)
app.include_router(analysis_router)
app.include_router(chat_router)

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "nsight-api"            
    }