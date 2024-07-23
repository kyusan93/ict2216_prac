import pytest, os, sys
from flask import Flask
import requests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../webapp')))
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SECRET_KEY'] = 'test_secret_key'
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_login_valid_password(client):
    # Test with a valid password (length >= 10 and not common)
    response = client.post('/', data={'password': 'ValidPassword123!'}, follow_redirects=True)
    assert response.status_code == 200
    # Check that there was one redirect response to the welcome page.
    assert len(response.history) == 1
    assert response.request.url == "http://localhost/welcome"

def test_login_invalid_password_too_short(client):
    # Test with an invalid password (less than 10 characters)
    response = client.post('/', data={'password': 'short'}, follow_redirects=True)
    assert response.status_code == 200
    # Check that there was no redirect response (stays on login page).
    assert len(response.history) == 0
    assert b'Password does not meet requirements or is too common.' in response.data

def test_login_invalid_password_non_printable(client):
    # Test with an invalid password containing non-printable characters
    response = client.post('/', data={'password': 'Valid\x00Password'}, follow_redirects=True)
    assert response.status_code == 200
    # Check that there was no redirect response (stays on login page).
    assert len(response.history) == 0
    assert b'Password does not meet requirements or is too common.' in response.data

def test_login_common_password(client):
    # Test with a common password
    response = client.post('/', data={'password': 'password'}, follow_redirects=True)
    assert response.status_code == 200
    # Check that there was no redirect response (stays on login page).
    assert len(response.history) == 0
    assert b'Password does not meet requirements or is too common.' in response.data

def test_login_password_with_spaces(client):
    # Test with a valid password that includes spaces
    response = client.post('/', data={'password': 'Valid Password 123'}, follow_redirects=True)
    assert response.status_code == 200
    # Check that there was one redirect response to the welcome page.
    assert len(response.history) == 1
    assert response.request.url == "http://localhost/welcome"

def test_logout(client):
    # Test logging out
    response = client.post('/', data={'password': 'ValidPassword123!'}, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.url == "http://localhost/welcome"
    
    # Log out and check that it redirects to the home page
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert response.request.url == "http://localhost/"

def test_login_empty_password(client):
    # Test with an empty password
    response = client.post('/', data={'password': ''}, follow_redirects=True)
    assert response.status_code == 200
    # Check that there was no redirect response (stays on login page).
    assert len(response.history) == 0
    assert b'Password does not meet requirements or is too common.' in response.data
