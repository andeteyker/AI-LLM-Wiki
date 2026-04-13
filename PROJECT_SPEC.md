# 🧠 AI-OS – Personal Knowledge & Assistant System

## 1. Vision

AI-OS ist ein lokales, später skalierbares System, das als persönlicher Assistent fungiert.

Ziel:
- Wissen speichern, strukturieren und nutzbar machen
- Dateien automatisch organisieren
- Notizen, Chats und Dokumente analysieren
- Aufgaben und Termine erkennen
- den Nutzer im Alltag aktiv unterstützen

Das System ersetzt:
- unstrukturierte Notizen
- chaotische Dateien
- verlorene Informationen

---

## 2. Grundprinzip

AI-OS ist KEIN Chatbot.

Es ist ein:

→ Knowledge Compiler System

Pipeline:
Raw Input → Analyse → Struktur → Speicherung → Nutzung → Feedback

---

## 3. Kernfunktionen (v1)

### Knowledge System
- Markdown-basierte Wissensdatenbank
- JSON-Metadaten
- automatische Verlinkung
- strukturierte Speicherung

### Chat
- Zugriff auf gesamtes Wissen
- Antworten mit:
  - Quellen
  - verknüpften Dateien
  - Vorschlägen

### Inbox
- ungeordnete Inhalte sammeln
- automatische Analyse
- Weiterverarbeitung

### Dashboard
- neue Einträge
- Aufgaben
- Termine
- offene Zuordnungen
- Systemhinweise

---

## 4. Datenquellen (v1)

- lokale Dateien
- PDFs
- Textdateien
- Bilder (Metadaten)
- Excel
- Chat-Exports

---

## 5. Informationsmodell

Jede Information wird klassifiziert als:

- Note
- Task
- Event
- File
- Project
- Person
- Topic
- Decision

Mehrere Typen gleichzeitig möglich.

---

## 6. Wissensspeicherung

Jeder Eintrag besteht aus:

### Markdown-Datei
- Titel
- Zusammenfassung
- Inhalt
- Verlinkungen

### JSON-Metadaten
- Typ
- Tags
- Quelle
- Beziehungen
- Confidence Score
- Zeitstempel

---

## 7. Ordnerstruktur

data/
├── inbox/
├── knowledge/
│   ├── arbeit/
│   ├── privat/
│   ├── projekte/
│   ├── wissensthemen/
│   ├── aufgaben/
│   ├── termine/
│   ├── personen/
│   ├── dateien/
│   └── archiv/
├── memory/
├── logs/
├── trash/

---

## 8. Systemarchitektur

### Ingestion Layer
- nimmt neue Daten auf
- extrahiert Inhalte
- erstellt Rohstruktur

### Knowledge Compiler
- analysiert Inhalte
- erstellt strukturierte Einträge
- verlinkt Informationen

### Assistant Layer
- Chat
- Dashboard
- Vorschläge
- Navigation

---

## 9. Agentensystem (v1)

### Manager Agent
- entscheidet über Verarbeitung
- delegiert Aufgaben

### Ingest Agent
- liest Dateien
- extrahiert Inhalte

### Knowledge Writer Agent
- erstellt Wissenseinträge

### Task/Planner Agent
- erkennt Aufgaben und Termine

---

## 10. Verhalten des Systems

### Standard
- automatische Analyse
- Mehrfachzuordnung
- Strukturaufbau

### Unsicherheit
- wird angezeigt
- Rückfragen möglich

### Widersprüche
- beide Versionen speichern
- Änderungen nachvollziehbar machen

---

## 11. Dateiverhalten

- automatische Klassifikation
- Umbenennung
- Verschiebung
- Duplikaterkennung

### Löschen
- nur über Papierkorb
- mit Log
- mit Begründung

---

## 12. Sicherheit

- Safe Mode
- Undo-Funktion
- vollständiges Logging
- keine irreversiblen Aktionen

---

## 13. UI

### Hauptbereiche
- Chat (Primär)
- Dashboard
- Inbox
- Wissen
- Aufgaben
- Termine
- Personen
- Dateien

### Anforderungen
- modern
- dark mode
- schnelle Navigation
- klare Übersicht

---

## 14. Prioritäten

### Wichtig
- automatische Verlinkung
- Zusammenfassungen

### Mittel
- Konflikterkennung

### Niedrig
- Versionierung

---

## 15. Erweiterungen (später)

- Microsoft Integration (Outlook, Teams)
- NAS / Server
- Multi-User
- Sprachsteuerung
- Mobile App

---

## 16. Technischer Stack

- Python
- FastAPI
- Streamlit
- Ollama
- Markdown + JSON Storage

---

## 17. Erfolgskriterien

- Notizen nicht mehr verloren
- Dateien auffindbar
- Aufgaben erkannt
- Termine nicht vergessen
- Wissen jederzeit abrufbar

---

## 18. No-Gos

- falsches Löschen
- unklare Entscheidungen
- zu kompliziert
- keine Transparenz

---

## 19. Designprinzipien

- Klarheit vor Komplexität
- Sicherheit vor Automation
- Struktur vor Geschwindigkeit
- Erweiterbarkeit

---

## 20. Zukunft

Ein vollständiges AI-OS als zweites Gehirn.
