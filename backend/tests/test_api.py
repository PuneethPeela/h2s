import os
import pytest
import mongomock

# Set environment variables before importing app
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
os.environ['JWT_SECRET_KEY'] = 'test-secret'

from app import app, db
import json
from mongoengine import connect, disconnect

@pytest.fixture(autouse=True)
def mock_mongo():
    disconnect()
    connect('test_db', host='localhost', mongo_client_class=mongomock.MongoClient)
    yield
    disconnect()

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'healthy'

def test_user_registration(client):
    """Test user registration."""
    data = {
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User"
    }
    response = client.post('/api/auth/register', json=data)
    assert response.status_code == 201
    assert response.get_json()['msg'] == 'User created successfully'

def test_user_login(client):
    """Test user login after registration."""
    # Register first
    client.post('/api/auth/register', json={
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User"
    })
    
    # Login
    response = client.post('/api/auth/login', json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert 'access_token' in response.get_json()

def test_symptom_check_requires_auth(client):
    """Test that symptom check endpoint is protected."""
    response = client.post('/api/ai/symptom-check', json={"symptoms": ["Fever"]})
    assert response.status_code == 401
