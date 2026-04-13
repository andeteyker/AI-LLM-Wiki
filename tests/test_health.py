from pathlib import Path

from fastapi.testclient import TestClient

from app.api.main import app


def test_health() -> None:
    client = TestClient(app)
    response = client.get('/health')
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'ok'
    assert 'safe_mode' in data


def test_ingest_search_chat_dashboard(tmp_path: Path) -> None:
    sample = tmp_path / 'projekt_roadmap.txt'
    sample.write_text('TODO: Roadmap abstimmen\nMeeting am Freitag mit Max Mustermann', encoding='utf-8')

    client = TestClient(app)
    ingest_response = client.post('/ingest', json={'path': str(sample)})
    assert ingest_response.status_code == 200
    payload = ingest_response.json()
    assert payload['status'] in {'confirmed', 'review_needed'}
    assert 'next_steps' in payload

    search_response = client.get('/search', params={'query': 'Roadmap'})
    assert search_response.status_code == 200
    results = search_response.json()
    assert isinstance(results, list)
    assert len(results) >= 1
    assert any('projekt roadmap' in item['title'].lower() for item in results)

    chat_response = client.post('/chat', json={'question': 'Was ist offen?'})
    assert chat_response.status_code == 200
    chat = chat_response.json()
    assert 'answer' in chat
    assert 'next_steps' in chat

    dashboard_response = client.get('/dashboard')
    assert dashboard_response.status_code == 200
    dashboard = dashboard_response.json()
    assert 'unresolved_links' in dashboard
    assert 'daily_report' in dashboard
