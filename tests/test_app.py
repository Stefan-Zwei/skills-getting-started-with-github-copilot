from urllib.parse import quote

from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200

    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"], dict)
    assert "participants" in data["Chess Club"]
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_participant_success():
    email = "testuser+signup@example.com"
    url = f"/activities/{quote('Chess Club')}/signup?email={quote(email)}"

    response = client.post(url)
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"

    response = client.get("/activities")
    assert email in response.json()["Chess Club"]["participants"]


def test_duplicate_signup_returns_400():
    email = "testuser+duplicate@example.com"
    url = f"/activities/{quote('Chess Club')}/signup?email={quote(email)}"

    response = client.post(url)
    assert response.status_code == 200

    duplicate_response = client.post(url)
    assert duplicate_response.status_code == 400
    assert duplicate_response.json()["detail"] == "Student is already signed up for this activity"


def test_unregister_participant_success():
    email = "testuser+remove@example.com"
    signup_url = f"/activities/{quote('Chess Club')}/signup?email={quote(email)}"
    delete_url = f"/activities/{quote('Chess Club')}/participants?email={quote(email)}"

    signup_response = client.post(signup_url)
    assert signup_response.status_code == 200

    delete_response = client.delete(delete_url)
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == f"Unregistered {email} from Chess Club"

    response = client.get("/activities")
    assert email not in response.json()["Chess Club"]["participants"]
