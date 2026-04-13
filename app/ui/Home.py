from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from app.agents.manager import ManagerAgent
from app.contacts.service import list_people
from app.core.adaptive import get_preferences, set_preferences
from app.core.bootstrap import ensure_runtime_layout
from app.dashboard.review import generate_daily_report
from app.dashboard.service import load_dashboard
from app.knowledge.query import answer_question, search_entries
from app.planner.events import list_events
from app.planner.projects import list_projects
from app.safety.duplicates import detect_duplicates
from app.safety.service import list_undo_actions
from app.tasks.engine import list_tasks

ensure_runtime_layout()

st.set_page_config(page_title="AI-OS", page_icon="🧠", layout="wide")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🧠 AI-OS")
st.caption("Knowledge-first Assistant")

dashboard = load_dashboard()
report = generate_daily_report()

chat_tab, dashboard_tab, inbox_tab, people_tab, projects_tab, review_tab, settings_tab = st.tabs(
    ["Chat", "Dashboard", "Inbox", "People", "Projects", "Review", "Settings"]
)

with chat_tab:
    question = st.chat_input("Frag dein Wissen...")
    if question:
        response = answer_question(question)
        st.session_state.chat_history.append((question, response))

    for question, response in reversed(st.session_state.chat_history[-10:]):
        with st.chat_message("user"):
            st.write(question)
        with st.chat_message("assistant"):
            st.write(response.answer)
            st.write("**Quellen**")
            for source in response.sources:
                st.write(f"- {source}")
            st.write("**Nächste Schritte**")
            for step in response.next_steps:
                st.write(f"- {step}")
            if response.uncertainty:
                st.warning(response.uncertainty)

    with st.expander("Suche"):
        query = st.text_input("Suchbegriff")
        type_filter = st.text_input("Filter Typ (optional)")
        project_filter = st.text_input("Filter Projekt (optional)")
        person_filter = st.text_input("Filter Person (optional)")
        if st.button("Suchen", use_container_width=True):
            for hit in search_entries(
                query=query,
                type_filter=type_filter or None,
                project_filter=project_filter or None,
                person_filter=person_filter or None,
            ):
                st.markdown(f"**{hit.title}** — Score {hit.score}")
                st.caption(f"{hit.source_path} · {hit.status}")
                st.write(hit.summary_short)

with dashboard_tab:
    c1, c2, c3 = st.columns(3)
    c1.metric("Neue Wissenseinträge", dashboard["knowledge_entries"])
    c2.metric("Neue Dateien", dashboard["new_files"])
    c3.metric("Offene Tasks", dashboard["open_tasks"])

    c4, c5, c6 = st.columns(3)
    c4.metric("Erkannte Termine", dashboard["detected_events"])
    c5.metric("Ungeklärte Zuordnungen", dashboard["unresolved_links"])
    c6.metric("Duplikatwarnungen", dashboard["duplicate_warnings"])

    st.metric("Personen/Kontakte", dashboard["people_contacts"])
    st.info(dashboard["daily_report"])

with inbox_tab:
    file_path = st.text_input("Dateipfad für Import")
    if st.button("Import starten", use_container_width=True):
        if not file_path:
            st.warning("Bitte Dateipfad angeben.")
        else:
            path = Path(file_path)
            if not path.exists():
                st.error("Datei nicht gefunden")
            else:
                result = ManagerAgent().ingest_path(path)
                st.success("Import abgeschlossen")
                st.json(result)

with people_tab:
    st.subheader("People Index")
    people = list_people()
    st.write(f"Einträge: {len(people)}")
    st.json(people)

with projects_tab:
    st.subheader("Project Index")
    projects = list_projects()
    st.write(f"Einträge: {len(projects)}")
    st.json(projects)

with review_tab:
    st.subheader("Daily Report")
    st.json(report)
    st.subheader("Offene Tasks")
    st.json(list_tasks(status="open"))
    st.subheader("Unklare Events")
    st.json(list_events(status="uncertain"))
    st.subheader("Duplikate")
    st.json(detect_duplicates())
    st.subheader("Undo Log")
    st.json(list_undo_actions())

with settings_tab:
    prefs = get_preferences()
    st.write("Aktuelle Präferenzen")
    st.json(prefs)
    style = st.selectbox("Antwortstil", ["practical", "brief", "detailed"], index=["practical", "brief", "detailed"].index(prefs.get("response_style", "practical")))
    if st.button("Präferenzen speichern"):
        updated = set_preferences({"response_style": style})
        st.success("Gespeichert")
        st.json(updated)
