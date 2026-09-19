from fastapi import FastAPI  # pyright: ignore[reportMissingImports]

app = FastAPI(
    title="Nsight API",
    version = "0.1.0"
)

@app.get("/health")

async def health():
    return {
        "status": "ok",
        "service": "nsight-api"            
    }