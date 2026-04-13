# Reuse Audit (Task 28)

## Directly adopted
- **FastAPI** for API routing and typed request/response.
- **Streamlit** for rapid local UI.
- **Pydantic / pydantic-settings** for validated models and env config.

## Conceptually inspired
- **Karpathy LLM Wiki Pattern**: markdown + metadata knowledge objects.
- **llm-wiki-compiler / wiki-langGraph ideas**: compile pipeline from raw docs to structured entries.
- **LangGraph/OpenClaw**: service-oriented orchestration boundaries prepared in `app/agents/services.py`.

## Intentionally not integrated yet
- Full LangGraph runtime orchestration.
- Deep OpenClaw memory/skill plumbing.
- External vector DB stack (Qdrant/Chroma).

Reason: first stabilize local-first, testable, transparent core before adding heavy dependencies.
