from __future__ import annotations

import json
from datetime import datetime

from app.core.settings import settings
from app.dashboard.service import load_dashboard
from app.tasks.engine import list_tasks
from app.planner.events import list_events

REPORT_DIR = settings.logs_dir / "reports"


def generate_daily_report() -> dict:
    dashboard = load_dashboard()
    tasks_open = list_tasks(status="open")
    uncertain_events = list_events(status="uncertain")

    report = {
        "date": datetime.utcnow().date().isoformat(),
        "new_things": {
            "new_files": dashboard.get("new_files", 0),
            "new_entries": dashboard.get("knowledge_entries", 0),
        },
        "open_things": {
            "open_tasks": len(tasks_open),
            "unresolved_links": dashboard.get("unresolved_links", 0),
        },
        "problematic_things": {
            "duplicate_warnings": dashboard.get("duplicate_warnings", 0),
            "uncertain_events": len(uncertain_events),
        },
        "recommended_next_steps": [
            "Review offene Zuordnungen",
            "Priorisierte Tasks planen",
            "Unklare Termine bestätigen",
        ],
        "delivery": {"prepared": True, "transport": "local_only"},
    }

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_file = REPORT_DIR / f"daily-{report['date']}.json"
    report_file.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report
