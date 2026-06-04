from fastapi.testclient import TestClient

from app import app, activities

client = TestClient(app)


def test_root_redirects_to_static_index():
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_signup_for_existing_activity():
    email = "new.student@mergington.edu"
    response = client.post(
        "/activities/Chess%20Club/signup",
        json={"email": email},
    )
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"


def test_signup_for_nonexistent_activity_returns_404():
    response = client.post(
        "/activities/Nonexistent/signup",
        json={"email": "test@mergington.edu"},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_duplicate_signup_returns_400():
    email = "michael@mergington.edu"
    response = client.post(
        "/activities/Chess%20Club/signup",
        json={"email": email},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up"


def test_activity_capacity_is_enforced():
    activity_name = "Test Club"
    activities[activity_name] = {
        "description": "A temporary activity for capacity test",
        "schedule": "Fridays, 4:00 PM",
        "max_participants": 1,
        "participants": [],
    }

    try:
        first_response = client.post(
            f"/activities/{activity_name}/signup",
            json={"email": "first.student@mergington.edu"},
        )
        assert first_response.status_code == 200

        second_response = client.post(
            f"/activities/{activity_name}/signup",
            json={"email": "second.student@mergington.edu"},
        )
        assert second_response.status_code == 400
        assert second_response.json()["detail"] == "Activity is full"
    finally:
        activities.pop(activity_name, None)
