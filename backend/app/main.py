from fastapi import FastAPI  # pyright: ignore[reportMissingImports]
from app.api.datasets import router as datasets_router

app = FastAPI(
    title="Nsight API",
    version = "0.1.0"
)


app.include_router(datasets_router)

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "nsight-api"            
    }