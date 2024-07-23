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
    response = client.post('/', data={'password': 'ValidPass123'}, follow_redirects=True)
    assert response.status_code == 200
    # Check that there was one redirect response.
    assert len(response.history) == 1
    assert response.request.url == "http://localhost/welcome"

def test_login_invalid_password(client):
    response = client.post('/', data={'password': 'short'}, follow_redirects=True)
    assert response.status_code == 200
    # Check that there was no redirect response (stays on login page).
    assert len(response.history) == 0
    assert b'Password does not meet requirements or is too common.' in response.data

def test_login_common_password(client):
    response = client.post('/', data={'password': 'password'}, follow_redirects=True)
    assert response.status_code == 200
    # Check that there was no redirect response (stays on login page).
    assert len(response.history) == 0
    assert b'Password does not meet requirements or is too common.' in response.data
