import pytest
from app import create_app
from app.extensions import db as _db


@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_register_success(client):
    response = client.post('/register', data={
        'name': 'Harmony Madisha',
        'email': 'harmony@example.com',
        'password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200


def test_register_duplicate_email(client):
    client.post('/register', data={
        'name': 'Harmony Madisha',
        'email': 'harmony@example.com',
        'password': 'password123'
    })
    response = client.post('/register', data={
        'name': 'Another User',
        'email': 'harmony@example.com',
        'password': 'password123'
    }, follow_redirects=True)
    assert b'already registered' in response.data


def test_register_missing_fields(client):
    response = client.post('/register', data={
        'name': '',
        'email': '',
        'password': ''
    }, follow_redirects=True)
    assert b'required' in response.data


def test_login_success(client):
    client.post('/register', data={
        'name': 'Harmony Madisha',
        'email': 'harmony@example.com',
        'password': 'password123'
    })
    response = client.post('/login', data={
        'email': 'harmony@example.com',
        'password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200


def test_login_wrong_password(client):
    client.post('/register', data={
        'name': 'Harmony Madisha',
        'email': 'harmony@example.com',
        'password': 'password123'
    })
    response = client.post('/login', data={
        'email': 'harmony@example.com',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    assert b'Invalid' in response.data


def test_login_unregistered_email(client):
    response = client.post('/login', data={
        'email': 'nobody@example.com',
        'password': 'password123'
    }, follow_redirects=True)
    assert b'Invalid' in response.data


def test_logout(client):
    client.post('/register', data={
        'name': 'Harmony Madisha',
        'email': 'harmony@example.com',
        'password': 'password123'
    })
    client.post('/login', data={
        'email': 'harmony@example.com',
        'password': 'password123'
    })
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
