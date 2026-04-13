# AI-OS v1 — Local Knowledge Operating System

AI-OS ist ein lokal-first System, das Dateien in strukturierte Wissenseinträge kompiliert und über API/UI such- und nutzbar macht.

## Architektur (aktuell)
- **Foundation:** zentrale Settings, Runtime-Bootstrap, strukturiertes Logging/Audit
- **Ingestion:** Parser-Registry + Parser (txt/md/json/csv/pdf + image/excel stubs)
- **Knowledge Core:** RawDocument -> KnowledgeEntry Compiler, Markdown/JSON Storage, Index/Relations
- **Search/Chat:** Filter-Suche + Retrieval-basierte Chat-Antworten, optionale Ollama-Anreicherung
- **Dashboard/Review:** täglicher Report, offene/problematische Dinge, Empfehlungen
- **Tasks/Events/People/Projects:** extrahierte Objekte und Indizes
- **Safety:** Duplikaterkennung, Organizer-Vorschläge (Safe Mode), Undo-Stack, Trash-Mechanik
- **Adaptive Layer:** persistente Präferenzen und Feedback-Hooks

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
cp .env.example .env
```

## Start
Backend:
```bash
uvicorn app.api.main:app --reload
```

UI:
```bash
streamlit run app/ui/Home.py
```

CLI Ingestion:
```bash
python scripts/ingest_file.py /pfad/zur/datei.txt
```

## API Überblick
- `GET /health`
- `POST /ingest`
- `GET /search`
- `POST /chat`
- `GET /dashboard`
- `GET /daily-report`
- `GET /inbox`
- `GET /tasks`
- `GET /events`
- `GET /people`
- `GET /projects`
- `GET /duplicates`
- `GET /undo`
- `GET/POST /preferences`
- `GET /behavior-rules`
- `POST /feedback`

## Datenfluss
1. Datei in Inbox importieren (Copy + Hash)
2. Parser erzeugt `RawDocument`
3. Compiler erzeugt `KnowledgeEntry`
4. Storage schreibt Markdown + JSON + Index
5. Task/Event/People/Project-Indizes werden aktualisiert
6. Dashboard/Review/Search/Chat greifen auf Index + Objektspeicher zu

## Offene Punkte
- Reprocess/Approve UI für Inbox ist als nächste Iteration vorgesehen.
- LLM-gestützte Extraktion ist derzeit nur als Hook vorbereitet.
- Fortgeschrittenes Ranking/semantische Suche kann erweitert werden.

## Nächste Schritte
- zusätzliche Tests für Safe-Mode-Organizer/Undo/Feedback-Flows
- bessere Datums-Parser für Events
- projektbezogene Knowledge-Seiten automatisiert generieren
- optionaler Versandkanal für Daily Reports (noch nicht integriert)

Siehe auch: `REUSE_AUDIT.md`.
