import pytest
from fastapi.testclient import TestClient
import copy
from src import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app.app)


@pytest.fixture
def sample_activities():
    """Return a fresh copy of sample activities data for testing."""
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        }
    }


@pytest.fixture(autouse=True)
def reset_activities(sample_activities):
    """Reset the activities data before each test to ensure isolation."""
    # Monkey patch the activities dict in the app module
    original_activities = app.activities
    app.activities = copy.deepcopy(sample_activities)
    yield
    # Restore original activities after test
    app.activities = original_activities