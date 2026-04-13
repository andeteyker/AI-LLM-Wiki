from __future__ import annotations

import logging
from pathlib import Path

from app.agents.services import IngestAgentService, KnowledgeWriterAgentService, TaskPlannerAgentService
from app.contacts.service import update_people_index
from app.planner.projects import update_project_index
from app.safety.organizer import suggest_organization
from app.safety.service import audit_log, error_log

agent_logger = logging.getLogger("agent_decisions")


class ManagerAgent:
    def __init__(self) -> None:
        self.ingest_agent = IngestAgentService()
        self.knowledge_agent = KnowledgeWriterAgentService()
        self.task_agent = TaskPlannerAgentService()

    def ingest_path(self, path: Path) -> dict:
        try:
            inbox_item, raw = self.ingest_agent.run(path)
            entry, (md_path, json_path) = self.knowledge_agent.run(raw)
            task_event_payload = self.task_agent.run(entry)
            update_people_index(entry)
            update_project_index(entry)
            organizer_hint = suggest_organization(Path(entry.source_path))

            result = {
                "inbox_item": inbox_item.model_dump(mode="json"),
                "raw_document_id": raw.id,
                "entry_id": entry.id,
                "markdown_path": str(md_path),
                "metadata_path": str(json_path),
                "status": entry.status,
                "open_questions": entry.open_questions,
                "next_steps": entry.next_steps,
                "tasks_created": len(task_event_payload["tasks"]),
                "events_created": len(task_event_payload["events"]),
                "organizer_suggestion": organizer_hint,
            }
            agent_logger.info("manager_pipeline completed for %s with status=%s", path, entry.status)
            audit_log(
                action="manager_pipeline",
                reason="ingest_compile_extract_index",
                source_path=str(path),
                target_path=str(json_path),
                confidence=entry.confidence,
                details={"status": entry.status},
            )
            return result
        except Exception as exc:
            error_log("manager.ingest_path", str(exc), {"path": str(path)})
            raise
