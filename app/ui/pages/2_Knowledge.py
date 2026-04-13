import streamlit as st
from app.core.bootstrap import ensure_runtime_layout
from app.core.settings import settings

ensure_runtime_layout()
st.title("Knowledge")
entries = sorted(settings.knowledge_dir.rglob("*.md"))
if not entries:
    st.info("No knowledge entries yet.")
else:
    for entry in entries:
        st.write(entry.relative_to(settings.knowledge_dir))
