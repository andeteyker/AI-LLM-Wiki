from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.agents.manager import ManagerAgent
from app.contacts.service import list_people
from app.core.adaptive import get_behavior_rules, get_preferences, record_feedback, set_preferences
from app.core.bootstrap import ensure_runtime_layout
from app.core.ollama import OllamaClient
from app.core.schemas import ChatAnswer, SearchResult
from app.core.settings import settings
from app.dashboard.review import generate_daily_report
from app.dashboard.service import load_dashboard
from app.knowledge.query import answer_question, search_entries
from app.planner.events import list_events
from app.planner.projects import list_projects
from app.safety.duplicates import detect_duplicates
from app.safety.service import list_undo_actions
from app.tasks.engine import list_tasks

ensure_runtime_layout()
app = FastAPI(title="AI-OS API", version="0.5.0")
manager = ManagerAgent()
ollama = OllamaClient()


class HealthResponse(BaseModel):
    status: str
    safe_mode: bool


class IngestRequest(BaseModel):
    path: str


class ChatRequest(BaseModel):
    question: str
    use_llm: bool = False


class PreferenceRequest(BaseModel):
    values: dict


class FeedbackRequest(BaseModel):
    event_type: str
    payload: dict


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", safe_mode=settings.safe_mode)


@app.get("/dashboard")
def dashboard() -> dict:
    return load_dashboard()


@app.get("/daily-report")
def daily_report() -> dict:
    return generate_daily_report()


@app.get("/inbox")
def inbox() -> dict:
    files = sorted(settings.inbox_dir.glob("*.json"))
    return {"count": len(files), "items": [json.loads(path.read_text(encoding="utf-8")) for path in files[-50:]]}


@app.post("/ingest")
def ingest_file(request: IngestRequest) -> dict:
    path = Path(request.path)
    if not path.exists() or not path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    return manager.ingest_path(path)


@app.get("/search", response_model=list[SearchResult])
def search(
    query: str = "",
    type_filter: str | None = None,
    project_filter: str | None = None,
    person_filter: str | None = None,
    source_filter: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
) -> list[SearchResult]:
    return search_entries(
        query=query,
        type_filter=type_filter,
        project_filter=project_filter,
        person_filter=person_filter,
        source_filter=source_filter,
        date_from=date_from,
        date_to=date_to,
    )


@app.post("/chat", response_model=ChatAnswer)
def chat(request: ChatRequest) -> ChatAnswer:
    base = answer_question(request.question)
    if request.use_llm:
        completion = ollama.generate(
            prompt=f"Frage: {request.question}\n\nKontext:\n{base.answer}",
            system="Du bist ein lokaler Wissensassistent. Antworte knapp und praktisch.",
        )
        if completion:
            base.answer = completion
    return base


@app.get("/tasks")
def tasks(status: str | None = None, priority: str | None = None) -> list[dict]:
    return list_tasks(status=status, priority=priority)


@app.get("/events")
def events(status: str | None = None) -> list[dict]:
    return list_events(status=status)


@app.get("/people")
def people() -> list[dict]:
    return list_people()


@app.get("/projects")
def projects() -> list[dict]:
    return list_projects()


@app.get("/duplicates")
def duplicates() -> list[dict]:
    return detect_duplicates()


@app.get("/undo")
def undo() -> list[dict]:
    return list_undo_actions()


@app.get("/preferences")
def preferences() -> dict:
    return get_preferences()


@app.post("/preferences")
def set_user_preferences(request: PreferenceRequest) -> dict:
    return set_preferences(request.values)


@app.get("/behavior-rules")
def behavior_rules() -> dict:
    return get_behavior_rules()


@app.post("/feedback")
def feedback(request: FeedbackRequest) -> dict:
    record_feedback(request.event_type, request.payload)
    return {"status": "recorded"}
