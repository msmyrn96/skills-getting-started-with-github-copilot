"""Tests for POST /activities/{activity_name}/signup endpoint."""
import pytest


def test_signup_success(client):
    """Test successful signup for an activity."""
    response = client.post("/activities/Chess%20Club/signup?email=newstudent@mergington.edu")

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Signed up newstudent@mergington.edu for Chess Club"

    # Verify the participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_duplicate_email(client):
    """Test signup with email already registered returns 400 error."""
    # First signup
    client.post("/activities/Chess%20Club/signup?email=duplicate@mergington.edu")

    # Second signup with same email should fail
    response = client.post("/activities/Chess%20Club/signup?email=duplicate@mergington.edu")

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student already signed up for this activity"


def test_signup_nonexistent_activity(client):
    """Test signup for non-existent activity returns 404 error."""
    response = client.post("/activities/NonExistent%20Activity/signup?email=test@mergington.edu")

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_signup_multiple_activities(client):
    """Test student can sign up for multiple different activities."""
    email = "multiactivity@mergington.edu"

    # Sign up for Chess Club
    response1 = client.post("/activities/Chess%20Club/signup?email=" + email)
    assert response1.status_code == 200

    # Sign up for Programming Class
    response2 = client.post("/activities/Programming%20Class/signup?email=" + email)
    assert response2.status_code == 200

    # Verify student is in both activities
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities["Chess Club"]["participants"]
    assert email in activities["Programming Class"]["participants"]


def test_signup_preserves_existing_participants(client):
    """Test that signup doesn't affect other participants."""
    # Sign up a new student
    client.post("/activities/Chess%20Club/signup?email=new@mergington.edu")

    # Check that existing participants are still there
    activities_response = client.get("/activities")
    activities = activities_response.json()
    chess_participants = activities["Chess Club"]["participants"]

    assert "michael@mergington.edu" in chess_participants
    assert "daniel@mergington.edu" in chess_participants
    assert "new@mergington.edu" in chess_participants
    assert len(chess_participants) == 3