# CODEX_HANDOFF.md

# AI-OS — vollständiger Handoff für Codex

## 0. Auftrag

Baue ein lokales, später skalierbares **AI-OS** als persönlichen Assistenten und Knowledge-Compiler.

Das System soll aus chaotischen Dateien, Notizen, Chats und Dokumenten eine strukturierte, durchsuchbare und nutzbare Wissensbasis erzeugen und darüber einen Assistenten bereitstellen, der:

- Wissen wiederfindbar macht
- Inhalte strukturiert speichert
- Beziehungen zwischen Themen, Projekten, Personen, Dateien, Aufgaben und Terminen erkennt
- Aufgaben und Termine aus Inhalten ableitet
- proaktiv auf Unklarheiten, Duplikate und neue relevante Inhalte hinweist
- sicher mit Daten umgeht
- lokal läuft
- später auf weitere Integrationen erweiterbar ist

WICHTIG:
- Nicht unnötig neu entwickeln.
- Vorhandene Open-Source-Bausteine maximal nutzen.
- Das System soll modular, wartbar und erweiterbar gebaut werden.
- Fokus auf ein starkes Fundament statt kurzlebiger Demo.

---

## 1. Produktvision

AI-OS ist **kein normaler Chatbot**.

Es ist ein hybrides System aus:

1. **Knowledge Compiler**
   - Rohdaten werden in dauerhaftes, strukturiertes Wissen überführt.

2. **Persönlicher Assistent**
   - Ein Chat- und Dashboard-zentriertes System, das Wissen nutzt, statt jede Anfrage nur neu zu beantworten.

3. **Adaptiver Agent**
   - Das System soll sich langfristig an den Nutzer anpassen.
   - Relevante Nutzerpräferenzen, Arbeitsmuster und Verhaltensregeln sollen persistent gespeichert und für bessere Entscheidungen genutzt werden.

---

## 2. Grundprinzip

### Rohinput → Analyse → Struktur → Wissensspeicherung → Nutzung → Feedback

Das System soll nicht nur RAG-artig Dokumente durchsuchen.

Stattdessen soll es:
- Inhalte kompilieren
- Wissen verdichten
- Verknüpfungen aufbauen
- Änderungen nachvollziehbar machen
- Fragen gegen die strukturierte Wissensbasis beantworten

---

## 3. Klare Produktziele

### 3.1 Primäre Ziele
- Notizen und Wissen sollen nicht verloren gehen
- Dateien sollen auffindbar und strukturiert werden
- Inhalte aus lokalen Quellen sollen automatisch in Wissen überführt werden
- Chat soll auf persönliches Wissen zugreifen
- Dashboard soll den Status des Systems sichtbar machen
- spätere Erweiterung zu Task-/Termin-/Kontakt-System vorbereiten

### 3.2 Sekundäre Ziele
- proaktive Hinweise
- Review-/Inbox-Konzept
- sichere Dateiverarbeitung
- später Microsoft-Integration
- später Multi-Geräte-/Server-Support

---

## 4. Projektumfang für v1

### Muss enthalten
- Web-UI
- Chat über eigenes Wissen
- Dashboard mit Inbox
- lokale Dateiintegration
- Parser für Standarddateitypen
- Knowledge Storage in Markdown + JSON
- Such-/Abrufschicht
- Entitäten: Note, Task, Event, File, Project, Person, Topic, Decision
- Logs
- Safe Mode
- Undo-/Trash-Konzept vorbereiten
- modulare Agentenstruktur intern

### Darf in v1 vorbereitet, aber noch nicht vollständig aktiv sein
- Microsoft-Integration
- externe Kalender-/Task-Synchronisation
- serverbasierte Ablage
- aggressive Auto-Dateioperationen über das gesamte System
- OCR/Bilderkennung auf hohem Niveau

---

## 5. Quellen für v1

Zuerst verarbeiten:
1. lokale Dateien
2. PDFs
3. Chats/Exports
4. einfache Text-/Markdown-Dateien
5. Bilder als Dateiobjekte + Metadaten
6. Excel-Dateien als Dateiobjekte + Basis-Metadaten

Noch nicht nötig in v1:
- Outlook live
- Teams live
- Planner live
- Microsoft To Do live

Diese Integrationen bitte architektonisch vorbereiten, aber noch nicht hart integrieren.

---

## 6. Nutzerverhalten / UX-Anforderungen

### 6.1 UI-Fokus
- modern
- dashboardartig
- dark mode standardmäßig
- Chat zuerst
- daneben oder darunter Status-/Dashboard-Informationen

### 6.2 Wichtigste UX-Ziele
- Übersicht
- schnelles Finden
- schöne, klare Darstellung
- nicht zu kompliziert

### 6.3 Was auf Startseite sichtbar sein soll
- Chat
- neue Dateien / Inbox
- neue Wissenseinträge
- ungeklärte Zuordnungen
- offene Aufgaben
- erkannte Termine
- relevante Personen/Kontakte
- täglicher Report / Systemhinweise

---

## 7. Wissensmodell

Das System soll das **empfohlene Wissensspeicherungsmodell** verwenden:

### 7.1 Speicherformen
- Markdown für lesbare Wiki-Einträge
- JSON für strukturierte Metadaten
- Relationen/Indizes für Verknüpfungen
- optional später Vector Memory

### 7.2 Hauptbereiche
Diese Hauptbereiche sollen initial angelegt werden:

- Inbox
- Arbeit
- Privat
- Projekte
- Wissensthemen
- Aufgaben
- Termine
- Personen
- Dateien
- Archiv

Die Struktur soll **hybrid** sein:
- feste Hauptbereiche
- dynamisch wachsende Unterbereiche

### 7.3 Objekt-Typen
Jeder Eintrag kann einer oder mehreren dieser Klassen angehören:

- Note
- Task
- Event
- File
- Project
- Person
- Topic
- Decision

Das System darf später zusätzliche Typen einführen, wenn bestehende Typen nicht ausreichen.

---

## 8. Anforderungen an einen Knowledge-Eintrag

Jeder Wissenseintrag soll kurz und ausführlich zugleich nutzbar sein:
- komprimiert genug für schnelle Übersicht
- detailliert genug, damit kein wichtiges Wissen verloren geht

### 8.1 Pflichtfelder
- id
- title
- summary_short
- summary_long
- content
- types
- tags
- source
- source_path
- created_at
- updated_at
- confidence
- related_projects
- related_people
- related_files
- related_topics
- extracted_tasks
- extracted_events
- open_questions
- next_steps
- version_info
- status

### 8.2 Speicherung
Pro Eintrag:
- 1 Markdown-Datei
- 1 JSON-Metadatei

### 8.3 Verlinkung
Automatische Verlinkung ist sehr wichtig.
Verlinke nach Möglichkeit:
- Projekte
- Personen
- Themen
- Dateien
- Aufgaben
- Termine

### 8.4 Quellen
Quellenangaben sind nützlich, aber nicht oberste Priorität.
Trotzdem immer speichern:
- Ursprung
- Pfad
- Dateityp
- Importzeitpunkt

### 8.5 Versionierung
Leichtgewichtige Versionierung:
- Änderungen nachvollziehbar
- ältere Stände einsehbar
- hybrid statt schwerem Git-Ersatz

---

## 9. Verhalten bei Widersprüchen und Unsicherheit

### 9.1 Unsicherheit
Wenn eine Klassifikation oder Zuordnung unsicher ist:
- Unsicherheit markieren
- Rückfrage ermöglichen
- mehrere Optionen zulassen

Nicht blind raten.

### 9.2 Widersprüche
Wenn neue Information bestehendem Wissen widerspricht:
- nicht einfach überschreiben
- beide Sichtweisen sichtbar halten
- neuere Information markieren
- Widerspruch kennzeichnen
- spätere Auflösung ermöglichen

### 9.3 Web-Recherche
Das System soll später optional Online-Recherche für Konfliktauflösung unterstützen.
Für v1 nur architektonisch vorbereiten, nicht zwingend voll implementieren.

---

## 10. Dateiverhalten

Später soll das System Dateien aktiv organisieren können.

Für v1 muss die Architektur darauf vorbereitet sein.

### Gewünschtes Zielverhalten
- automatisch taggen
- automatisch einsortieren
- automatisch umbenennen
- Duplikate erkennen
- Löschvorschläge machen

### Sicherheitsregeln
- kein hartes Löschen
- potenzielle Löschung nur via Papierkorb/Trash
- Log mit:
  - was gelöscht/verschoben wurde
  - warum
  - woher
  - wohin
  - wann

### Aggressivität
Mittel
- hilfreich
- aber nicht gefährlich

---

## 11. Chat-Verhalten

Der Chat soll **Assistent + Wissenssucher** sein.

### Pflichtverhalten
Bei Wissensfragen:
- direkte Antwort geben
- verknüpfte Dateien/Notizen anzeigen
- sinnvolle nächste Schritte vorschlagen

### Bei Unsicherheit
- Unsicherheit offen anzeigen
- bei Bedarf Rückfrage stellen

### Ziel
Nicht nur Informationen wiederholen, sondern:
- Zusammenhänge erkennen
- relevante Dinge verlinken
- Nutzen erzeugen

### Stil
- klar
- brauchbar
- nicht unnötig kompliziert

---

## 12. Anpassung / Lernverhalten

Das System soll sich langfristig an den Nutzer anpassen.

WICHTIG:
- Wenn OpenClaw / verwandte Open-Source-Komponenten dieses Verhalten bereits gut abdecken, sollen diese genutzt und nicht neu erfunden werden.
- Nur fehlende Teile ergänzen.

### Gewünschte Richtung
- persistente Nutzerpräferenzen
- Regel-/Verhaltenslayer
- selbst lernende Verbesserung über Zeit
- Anpassung an Arbeitsstil und Bedürfnisse des Nutzers

### Beispiele
- bevorzugte Antwortform
- bevorzugte Dateiorganisation
- bevorzugte Eingriffstiefe
- typische Muster (z. B. chaotische Downloads, verlorene Notizen, vergessene Termine)

Bitte dafür eine **saubere, modulare Character-/Behavior-/Preference-Schicht** vorsehen.

---

## 13. Open-Source-Reuse-Strategie

Es sollen so viele bestehende Open-Source-Projekte wie sinnvoll genutzt werden.
Das Rad nicht neu erfinden.

### Bereits bekannte Inspirations-/Reuse-Kandidaten
- OpenClaw / ClawHub / Skill-Ökosystem
- Karpathy LLM Wiki Pattern
- wiki-langGraph
- llm-wiki-compiler
- LangGraph
- Ollama
- Chroma/Qdrant optional später
- Watchdog für Dateibeobachtung
- Streamlit für v1 UI

### Codex soll aktiv prüfen
- welche dieser Projekte direkt eingebunden werden können
- welche Konzepte statt Code-Reuse sinnvoller sind
- welche Teile wir wirklich selbst bauen müssen

### Wichtig
Bitte nicht blind alles integrieren.
Nur übernehmen, was:
- stabil
- verständlich
- wartbar
- lokal nutzbar
- lizenztechnisch unproblematisch
ist.

---

## 14. Zielarchitektur

Das System soll modular aufgebaut sein.

### 14.1 Ebenen

#### A. Ingestion Layer
Verantwortlich für:
- Dateiaufnahme
- Rohtext-/Metadatenextraktion
- erste Einordnung

#### B. Knowledge Compiler
Verantwortlich für:
- Klassifikation
- Entitätserkennung
- Zusammenfassung
- Verlinkung
- Markdown/JSON-Erzeugung

#### C. Retrieval / Query Layer
Verantwortlich für:
- Suche
- Filter
- Chat-Antwortgrundlage
- Relationen abrufen

#### D. Assistant Layer
Verantwortlich für:
- Chat
- Dashboard
- Inbox
- Review
- nächste Schritte / Hinweise

#### E. Safety Layer
Verantwortlich für:
- Logs
- Safe Mode
- Undo-/Trash-Mechanik
- transparente Aktionen

---

## 15. Agentenstruktur

Bitte für v1 intern diese Agentenrollen vorsehen:

### 15.1 Manager Agent
- entscheidet, welche Pipeline verwendet wird
- verteilt Aufgaben
- priorisiert

### 15.2 Ingest Agent
- nimmt Inputs entgegen
- extrahiert Inhalte / Metadaten
- legt Inbox-Eintrag an

### 15.3 Knowledge Writer Agent
- erzeugt Wissenseinträge
- baut Links / Beziehungen

### 15.4 Task/Planner Agent
- erkennt Aufgaben und Termine
- speichert sie intern
- externe Integrationen später

Diese Rollen dürfen in v1 technisch auch erstmal als Services / Module statt „voll autonomer Agenten“ implementiert werden, solange die spätere Erweiterung möglich bleibt.

---

## 16. Startstruktur im Repository

Bitte diese Startstruktur einhalten oder sehr nah daran bleiben:

```text
ai-os/
├─ app/
│  ├─ agents/
│  ├─ api/
│  ├─ core/
│  ├─ ingestion/
│  ├─ knowledge/
│  ├─ tasks/
│  ├─ planner/
│  ├─ contacts/
│  ├─ dashboard/
│  └─ safety/
├─ data/
│  ├─ inbox/
│  ├─ knowledge/
│  │  ├─ arbeit/
│  │  ├─ privat/
│  │  ├─ projekte/
│  │  ├─ wissensthemen/
│  │  ├─ aufgaben/
│  │  ├─ termine/
│  │  ├─ personen/
│  │  ├─ dateien/
│  │  └─ archiv/
│  ├─ memory/
│  ├─ logs/
│  ├─ trash/
│  └─ cache/
├─ config/
├─ scripts/
├─ tests/
└─ run.py
```

---

## 17. Technologieentscheidungen

### Für v1 bevorzugt
- Python
- FastAPI
- Streamlit
- Ollama
- Markdown + JSON
- lokale Dateispeicherung
- modulare Services
- optionale SQLite für Indizes / Metadaten, falls sinnvoll

### Später möglich
- Qdrant / Chroma
- React/Next.js
- Microsoft Graph
- NAS/Server
- Multi-User

---

## 18. Konkrete Erwartungen an Codex

### 18.1 Nicht tun
- kein wildes Overengineering
- keine unnötigen Frameworks
- keine instabile halbe Integration von 10 Fremdprojekten
- kein riesiges abstraktes Agentensystem ohne Nutzen
- nicht das ganze Produkt neu interpretieren

### 18.2 Tun
- pragmatisch bauen
- gut strukturieren
- wiederverwendbare Module
- klare Datenmodelle
- verständliche README und Dokumentation
- saubere Logs
- gute Defaults
- gute Erweiterbarkeit

### 18.3 Wenn unklar
Bei Unklarheiten bitte:
- konservative, sinnvolle Architekturentscheidungen treffen
- an Erweiterbarkeit denken
- Sicherheit und Einfachheit priorisieren

---

## 19. Priorisierte Lieferreihenfolge

### Phase 1 — stabiles Fundament
- Projektgerüst
- Settings / Config
- Datenordner
- Logging
- API-Basis
- Streamlit-Basis
- grundlegende Navigation
- Inbox / Knowledge / Chat Grundseiten

### Phase 2 — Knowledge Core
- Datei-Ingestion
- Parser für txt, md, pdf, json, csv
- Basisparser für Bilder / Excel-Metadaten
- Klassifikation
- Knowledge-Eintrag-Erstellung
- Markdown + JSON Speicherung
- einfacher Index

### Phase 3 — Retrieval und Chat
- Suche
- Filter
- Antwortaufbereitung
- Quellen / verknüpfte Einträge
- nächste Schritte

### Phase 4 — Dashboard / Review
- Inbox-Status
- neue Einträge
- offene Zuordnungen
- erkannte Tasks / Events
- Warnungen / Hinweise

### Phase 5 — Adaptivität / Verhalten
- Preference-/Behavior-Schicht
- Review-Mechanik
- proaktive Hinweise
- Erweiterbarkeit Richtung OpenClaw-/Memory-Layer

---

## 20. Akzeptanzkriterien für v1

v1 ist erfolgreich, wenn:

1. Ein Nutzer lokale Dateien oder PDFs in das System geben kann.
2. Das System daraus strukturierte Wissenseinträge erzeugt.
3. Diese Einträge in Markdown + JSON gespeichert werden.
4. Der Nutzer über Chat nach eigenem Wissen fragen kann.
5. Antworten relevante verknüpfte Inhalte anzeigen.
6. Das Dashboard neue und ungeklärte Inhalte sichtbar macht.
7. Das System logisch, stabil und lokal nutzbar ist.
8. Die Architektur so sauber ist, dass weitere Integrationen später möglich sind.

---

## 21. No-Gos

- falsches oder irreversibles Löschen
- unnötig komplizierte Bedienung
- fehlende Transparenz
- nur Demo ohne belastbare Struktur
- Chat ohne echte Wissensbasis
- Wissen ohne Nachvollziehbarkeit

---

## 22. Erste konkrete Arbeitsanweisung an Codex

Bitte bearbeite das Projekt in dieser Reihenfolge:

### Schritt 1
Analysiere die bestehende Projektstruktur und prüfe, was schon vorhanden ist.

### Schritt 2
Bringe das Repository in eine saubere, lauffähige v1-Grundstruktur.

### Schritt 3
Implementiere den stabilen Knowledge Core:
- Ingestion
- Parsing
- Klassifikation
- Speicherung als Markdown + JSON

### Schritt 4
Implementiere Chat + Dashboard auf Basis der gespeicherten Wissensbasis.

### Schritt 5
Dokumentiere:
- Architektur
- Start
- Datenfluss
- Erweiterungspunkte

### Schritt 6
Markiere klar:
- was direkt übernommen wurde
- was inspiriert ist
- was Eigenbau ist

---

## 23. Bonus: Gewünschte Ausgabe von Codex

Codex soll nach Möglichkeit zusätzlich liefern:

- aktualisierte README
- klare Setup-Anleitung
- Liste offener Punkte / TODOs
- Liste empfohlener nächster Schritte
- Begründung größerer Architekturentscheidungen

---

## 24. Wichtigster Leitsatz

Baue ein **echtes, lokales, erweiterbares AI-OS-Fundament** —
kein Spielzeug, keine reine Demo, kein unnötig überkomplexes Agentenexperiment.

