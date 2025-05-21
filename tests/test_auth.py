import json
import pytest

def test_home_route(client):
    """Test the home route"""
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert data['message'] == 'Welcome to the Home Page'

def test_user_registration(client, cleanup_test_data):
    """Test user registration"""
    # Valid registration
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword123',
        'first_name': 'Test',
        'last_name': 'User'
    }
    
    response = client.post('/register', 
        data=json.dumps(user_data),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'user_id' in data
    assert 'message' in data
    assert data['message'] == 'User registered successfully'

def test_invalid_registration(client):
    """Test invalid registration scenarios"""
    # Missing fields
    response = client.post('/register', 
        data=json.dumps({}),
        content_type='application/json'
    )
    assert response.status_code == 400

    # Invalid email
    invalid_email_data = {
        'username': 'invaliduser',
        'email': 'invalidemail',
        'password': 'password123'
    }
    response = client.post('/register', 
        data=json.dumps(invalid_email_data),
        content_type='application/json'
    )
    assert response.status_code == 400

    # Short password
    short_pass_data = {
        'username': 'shortpass',
        'email': 'short@example.com',
        'password': '123'
    }
    response = client.post('/register', 
        data=json.dumps(short_pass_data),
        content_type='application/json'
    )
    assert response.status_code == 400

def test_user_login(client):
    """Test user login"""
    # First, register a user
    user_data = {
        'username': 'loginuser',
        'email': 'login@example.com',
        'password': 'loginpassword123'
    }
    
    client.post('/register', 
        data=json.dumps(user_data),
        content_type='application/json'
    )
    
    # Then try to login
    login_response = client.post('/login', 
        data=json.dumps({
            'username': user_data['username'],
            'password': user_data['password']
        }),
        content_type='application/json'
    )
    
    assert login_response.status_code == 200
    login_data = json.loads(login_response.data)
    assert 'access_token' in login_data

def test_invalid_login(client):
    """Test invalid login scenarios"""
    # Non-existent user
    response = client.post('/login', 
        data=json.dumps({
            'username': 'nonexistentuser',
            'password': 'wrongpassword'
        }),
        content_type='application/json'
    )
    assert response.status_code == 401

    # Missing credentials
    response = client.post('/login', 
        data=json.dumps({}),
        content_type='application/json'
    )
    assert response.status_code == 400 