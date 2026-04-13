import streamlit as st
from app.core.bootstrap import ensure_runtime_layout
from app.core.settings import settings

ensure_runtime_layout()
st.title("Inbox")
files = sorted(settings.inbox_dir.glob("*"))
if not files:
    st.info("Inbox is empty.")
else:
    for f in files:
        st.write(f.name)
