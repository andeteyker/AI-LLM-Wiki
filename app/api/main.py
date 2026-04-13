from fastapi import FastAPI
from pydantic import BaseModel

from app.core.bootstrap import ensure_runtime_layout
from app.core.settings import settings

ensure_runtime_layout()
app = FastAPI(title="AI-OS API", version="0.1.0")


class HealthResponse(BaseModel):
    status: str
    safe_mode: bool


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", safe_mode=settings.safe_mode)
