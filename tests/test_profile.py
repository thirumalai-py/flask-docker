import json
import pytest

def test_get_profile(client, jwt_token):
    """Test retrieving user profile"""
    response = client.get('/profile', 
        headers={'Authorization': f'Bearer {jwt_token}'}
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    # Check profile fields
    assert 'username' in data
    assert 'email' in data
    assert data['username'] == 'testuser'
    assert data['email'] == 'test@example.com'

def test_update_profile(client, jwt_token):
    """Test updating user profile"""
    update_data = {
        'first_name': 'Updated',
        'last_name': 'Name'
    }
    
    response = client.put('/profile', 
        data=json.dumps(update_data),
        content_type='application/json',
        headers={'Authorization': f'Bearer {jwt_token}'}
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    # Verify updated fields
    assert data['first_name'] == 'Updated'
    assert data['last_name'] == 'Name'

def test_change_password(client, jwt_token):
    """Test changing user password"""
    change_password_data = {
        'current_password': 'testpassword123',
        'new_password': 'newpassword456'
    }
    
    response = client.post('/change-password', 
        data=json.dumps(change_password_data),
        content_type='application/json',
        headers={'Authorization': f'Bearer {jwt_token}'}
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Password changed successfully'

def test_change_password_invalid(client, jwt_token):
    """Test invalid password change scenarios"""
    # Wrong current password
    wrong_current_pass = {
        'current_password': 'wrongpassword',
        'new_password': 'newpassword456'
    }
    
    response = client.post('/change-password', 
        data=json.dumps(wrong_current_pass),
        content_type='application/json',
        headers={'Authorization': f'Bearer {jwt_token}'}
    )
    
    assert response.status_code == 400

    # Short new password
    short_new_pass = {
        'current_password': 'testpassword123',
        'new_password': '123'
    }
    
    response = client.post('/change-password', 
        data=json.dumps(short_new_pass),
        content_type='application/json',
        headers={'Authorization': f'Bearer {jwt_token}'}
    )
    
    assert response.status_code == 400

def test_unauthorized_access(client):
    """Test accessing protected routes without authentication"""
    # Get profile without token
    response = client.get('/profile')
    assert response.status_code == 401

    # Update profile without token
    response = client.put('/profile', 
        data=json.dumps({'first_name': 'Test'}),
        content_type='application/json'
    )
    assert response.status_code == 401

    # Change password without token
    response = client.post('/change-password', 
        data=json.dumps({
            'current_password': 'oldpass',
            'new_password': 'newpass'
        }),
        content_type='application/json'
    )
    assert response.status_code == 401 