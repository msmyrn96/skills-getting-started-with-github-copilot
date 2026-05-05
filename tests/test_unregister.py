"""Tests for DELETE /activities/{activity_name}/unregister endpoint."""
import pytest


def test_unregister_success(client):
    """Test successful unregister from an activity."""
    response = client.delete("/activities/Chess%20Club/unregister?email=michael@mergington.edu")

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Unregistered michael@mergington.edu from Chess Club"

    # Verify the participant was removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
    assert "daniel@mergington.edu" in activities["Chess Club"]["participants"]  # Other participant still there


def test_unregister_nonexistent_participant(client):
    """Test unregister with email not registered returns 400 error."""
    response = client.delete("/activities/Chess%20Club/unregister?email=notregistered@mergington.edu")

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student not registered for this activity"


def test_unregister_nonexistent_activity(client):
    """Test unregister from non-existent activity returns 404 error."""
    response = client.delete("/activities/NonExistent%20Activity/unregister?email=test@mergington.edu")

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_unregister_preserves_other_participants(client):
    """Test that unregister doesn't affect other participants."""
    # Unregister one participant
    client.delete("/activities/Chess%20Club/unregister?email=michael@mergington.edu")

    # Check that other participant is still there
    activities_response = client.get("/activities")
    activities = activities_response.json()
    chess_participants = activities["Chess Club"]["participants"]

    assert "michael@mergington.edu" not in chess_participants
    assert "daniel@mergington.edu" in chess_participants
    assert len(chess_participants) == 1


def test_unregister_then_reregister(client):
    """Test that a student can unregister and then register again."""
    email = "test@mergington.edu"

    # Register
    client.post("/activities/Chess%20Club/signup?email=" + email)

    # Verify registered
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities["Chess Club"]["participants"]

    # Unregister
    client.delete("/activities/Chess%20Club/unregister?email=" + email)

    # Verify unregistered
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email not in activities["Chess Club"]["participants"]

    # Register again
    client.post("/activities/Chess%20Club/signup?email=" + email)

    # Verify registered again
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities["Chess Club"]["participants"]