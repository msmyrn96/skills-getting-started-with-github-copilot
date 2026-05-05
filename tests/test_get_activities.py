"""Tests for GET /activities endpoint."""
import pytest
from fastapi.responses import RedirectResponse


def test_get_activities_success(client, sample_activities):
    """Test successful retrieval of all activities."""
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()

    # Verify we get all activities
    assert len(data) == len(sample_activities)

    # Verify expected activity names are present
    expected_activities = ["Chess Club", "Programming Class", "Gym Class"]
    assert set(data.keys()) == set(expected_activities)

    # Verify structure of each activity
    for activity_name, activity_data in data.items():
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participants" in activity_data
        assert isinstance(activity_data["participants"], list)


def test_get_activities_chess_club_details(client):
    """Test specific details of Chess Club activity."""
    response = client.get("/activities")
    data = response.json()

    chess_club = data["Chess Club"]
    assert chess_club["description"] == "Learn strategies and compete in chess tournaments"
    assert chess_club["schedule"] == "Fridays, 3:30 PM - 5:00 PM"
    assert chess_club["max_participants"] == 12
    assert chess_club["participants"] == ["michael@mergington.edu", "daniel@mergington.edu"]


def test_get_activities_programming_class_details(client):
    """Test specific details of Programming Class activity."""
    response = client.get("/activities")
    data = response.json()

    programming_class = data["Programming Class"]
    assert programming_class["description"] == "Learn programming fundamentals and build software projects"
    assert programming_class["schedule"] == "Tuesdays and Thursdays, 3:30 PM - 4:30 PM"
    assert programming_class["max_participants"] == 20
    assert programming_class["participants"] == ["emma@mergington.edu", "sophia@mergington.edu"]


def test_get_activities_gym_class_details(client):
    """Test specific details of Gym Class activity."""
    response = client.get("/activities")
    data = response.json()

    gym_class = data["Gym Class"]
    assert gym_class["description"] == "Physical education and sports activities"
    assert gym_class["schedule"] == "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM"
    assert gym_class["max_participants"] == 30
    assert gym_class["participants"] == ["john@mergington.edu", "olivia@mergington.edu"]


def test_root_redirect(client):
    """Test that root endpoint redirects to static index page."""
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307  # Temporary redirect
    assert response.headers["location"] == "/static/index.html"