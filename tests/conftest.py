import os
import pytest
import sys
import json

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app as flask_app
from pymongo import MongoClient

# Get MongoDB URI from environment variable
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/test_db')

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db_name = MONGO_URI.split('/')[-1]
db = client[db_name]

@pytest.fixture
def app():
    """Fixture for Flask app"""
    flask_app.config['TESTING'] = True
    return flask_app

@pytest.fixture
def client(app):
    """Test client for making requests"""
    return app.test_client()

@pytest.fixture
def jwt_token(client):
    """Generate a JWT token for authenticated tests"""
    # Create a test user first
    test_user = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword123'
    }
    
    # Register the user
    register_response = client.post('/register', 
        data=json.dumps(test_user),
        content_type='application/json'
    )
    
    # Login to get the token
    login_response = client.post('/login', 
        data=json.dumps({
            'username': test_user['username'],
            'password': test_user['password']
        }),
        content_type='application/json'
    )
    
    # Return the token
    login_data = json.loads(login_response.data)
    return login_data.get('access_token')

@pytest.fixture
def cleanup_test_data():
    """Cleanup test data after tests"""
    yield
    # Remove test user from database
    db.users.delete_many({
        'username': 'testuser',
        'email': 'test@example.com'
    }) 