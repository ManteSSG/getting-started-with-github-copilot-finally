import pytest


def test_get_activities(client):
    """Test GET /activities returns all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert data["Chess Club"]["max_participants"] == 12
    assert "michael@mergington.edu" in data["Chess Club"]["participants"]


def test_signup_success(client):
    """Test successful signup for an activity"""
    response = client.post(
        "/activities/Chess Club/signup?email=newstudent@mergington.edu"
    )
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]
    
    # Verify participant was added
    activities = client.get("/activities").json()
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_duplicate(client):
    """Test signup fails for duplicate email"""
    response = client.post(
        "/activities/Chess Club/signup?email=michael@mergington.edu"
    )
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]


def test_signup_nonexistent_activity(client):
    """Test signup fails for non-existent activity"""
    response = client.post(
        "/activities/Fake Club/signup?email=student@mergington.edu"
    )
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"]


def test_unregister_success(client):
    """Test successful unregister from an activity"""
    response = client.delete(
        "/activities/Chess Club/unregister?email=michael@mergington.edu"
    )
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered" in data["message"]
    
    # Verify participant was removed
    activities = client.get("/activities").json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_not_registered(client):
    """Test unregister fails for non-registered student"""
    response = client.delete(
        "/activities/Chess Club/unregister?email=notmember@mergington.edu"
    )
    assert response.status_code == 400
    data = response.json()
    assert "not registered" in data["detail"]


def test_unregister_nonexistent_activity(client):
    """Test unregister fails for non-existent activity"""
    response = client.delete(
        "/activities/Fake Club/unregister?email=student@mergington.edu"
    )
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"]
