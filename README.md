# AI-OS v1 Scaffold

Local-first AI-OS scaffold for personal knowledge management, inbox processing, and assistant workflows.

## Goals for v1
- Chat over own knowledge
- Wiki-style knowledge base
- Dashboard with inbox
- Safe local-first operation
- Structured storage in Markdown + JSON metadata

## Tech choices for v1
- Python 3.11+
- FastAPI backend
- Streamlit web UI
- Local storage in files
- Optional Ollama integration

## Project structure
- `app/agents/` orchestration roles
- `app/api/` backend routes
- `app/core/` settings, logging, schemas
- `app/ingestion/` file ingestion and parsing
- `app/knowledge/` knowledge compiler and index
- `app/tasks/` tasks and event extraction
- `app/dashboard/` report/dashboard helpers
- `app/ui/` Streamlit interface
- `data/` runtime storage
- `config/` yaml/json config files

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or .venv\\Scripts\\activate on Windows
pip install -e .
copy .env.example .env  # Windows
# or cp .env.example .env
streamlit run app/ui/Home.py
```

## Next implementation steps
1. Wire settings and paths
2. Implement ingest pipeline for txt/md/pdf/json/csv
3. Write knowledge entries as markdown + metadata json
4. Add search/index
5. Add chat over knowledge and Ollama integration
