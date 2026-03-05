import pytest
from fastapi.testclient import TestClient
from copy import deepcopy
import sys
from pathlib import Path

# Add src to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture
def fresh_activities():
    """Provide a fresh copy of activities for each test"""
    return deepcopy(activities)


@pytest.fixture
def client(fresh_activities, monkeypatch):
    """Create a test client with isolated activities data"""
    monkeypatch.setattr("app.activities", fresh_activities)
    return TestClient(app)
