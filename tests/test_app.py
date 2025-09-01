import pytest
from app import create_app
from models import db

@pytest.fixture()
def client():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
        "SECRET_KEY": "test"
    })
    with app.app_context():
        db.drop_all()
        db.create_all()
    with app.test_client() as client:
        yield client

def test_event_crud(client):
    # Register
    r = client.post("/auth/register", json={"name": "Test", "email": "t@example.com", "password": "secret123"})
    assert r.status_code in (200, 201)

    # Create
    payload = {
        "title": "My Event",
        "description": "Desc",
        "city": "Hyderabad",
        "start_time": "2025-08-27T18:30:00",
        "organizer_name": "Me"
    }
    r = client.post("/events", json=payload)
    assert r.status_code == 201
    ev_id = r.get_json()["event"]["id"]

    # List
    r = client.get("/events")
    assert r.status_code == 200
    assert len(r.get_json()) == 1

    # Update
    payload["title"] = "Updated Title"
    r = client.put(f"/events/{ev_id}", json=payload)
    assert r.status_code == 200
    assert r.get_json()["event"]["title"] == "Updated Title"

    # Delete
    r = client.delete(f"/events/{ev_id}")
    assert r.status_code == 200
