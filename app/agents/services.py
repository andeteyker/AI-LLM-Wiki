from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from app.core.schemas import KnowledgeEntry, RawDocument
from app.ingestion.service import ingest_file
from app.knowledge.compiler import compile_document
from app.knowledge.storage import save_entry
from app.planner.events import EventExtractionEngine, save_events
from app.tasks.engine import TaskExtractionEngine, save_tasks


class AgentService(ABC):
    @abstractmethod
    def run(self, payload):
        raise NotImplementedError


class IngestAgentService(AgentService):
    def run(self, payload: Path):
        return ingest_file(payload)


class KnowledgeWriterAgentService(AgentService):
    def run(self, payload: RawDocument) -> tuple[KnowledgeEntry, tuple[Path, Path]]:
        entry = compile_document(payload)
        paths = save_entry(entry)
        return entry, paths


class TaskPlannerAgentService(AgentService):
    def __init__(self) -> None:
        self.task_engine = TaskExtractionEngine()
        self.event_engine = EventExtractionEngine()

    def run(self, payload: KnowledgeEntry) -> dict:
        tasks = self.task_engine.extract(payload)
        events = self.event_engine.extract(payload)
        save_tasks(tasks)
        save_events(events)
        return {
            "tasks": [task.model_dump() for task in tasks],
            "events": [event.model_dump() for event in events],
        }
