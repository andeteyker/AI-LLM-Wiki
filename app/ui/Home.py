import streamlit as st
from pathlib import Path

from app.core.bootstrap import ensure_runtime_layout
from app.core.settings import settings

ensure_runtime_layout()

st.set_page_config(page_title="AI-OS", page_icon="🧠", layout="wide")

st.title("🧠 AI-OS")
st.caption("Local-first knowledge assistant scaffold")

left, right = st.columns([2, 1])
with left:
    st.subheader("Chat")
    st.info("Chat over your knowledge base will be wired here next.")
    prompt = st.text_input("Ask your knowledge base", placeholder="What do I already know about project X?")
    if prompt:
        st.write("Placeholder response:", f"You asked: {prompt}")

with right:
    st.subheader("Today")
    st.metric("Safe Mode", "On" if settings.safe_mode else "Off")
    st.metric("Inbox files", len(list((settings.inbox_dir).glob("*"))))
    st.metric("Knowledge entries", len(list((settings.knowledge_dir).rglob("*.md"))))

st.divider()

st.subheader("Quick navigation")
col1, col2, col3, col4 = st.columns(4)
col1.button("Inbox", use_container_width=True)
col2.button("Knowledge", use_container_width=True)
col3.button("Tasks", use_container_width=True)
col4.button("Logs", use_container_width=True)

st.subheader("Knowledge folders")
for folder in sorted([p for p in settings.knowledge_dir.iterdir() if p.is_dir()]):
    st.write(f"- {folder.name}")
