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


@pytest.fixture
def logged_in_client(client):
    client.post('/register', data={
        'name': 'Harmony Madisha',
        'email': 'harmony@example.com',
        'password': 'password123'
    })
    client.post('/login', data={
        'email': 'harmony@example.com',
        'password': 'password123'
    })
    return client


def test_create_project_success(logged_in_client):
    response = logged_in_client.post('/projects/new', data={
        'title': 'Mzansi Eats',
        'description': 'A food delivery app for South Africa',
        'stage': 'Prototype',
        'support_required': 'Frontend help'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Mzansi Eats' in response.data


def test_create_project_missing_fields(logged_in_client):
    response = logged_in_client.post('/projects/new', data={
        'title': '',
        'description': '',
        'stage': '',
        'support_required': ''
    }, follow_redirects=True)
    assert b'required' in response.data


def test_create_project_requires_login(client):
    response = client.post('/projects/new', data={
        'title': 'Mzansi Eats',
        'description': 'A food delivery app',
        'stage': 'Prototype',
        'support_required': 'Frontend help'
    }, follow_redirects=True)
    assert b'Login' in response.data


def test_feed_shows_projects(logged_in_client):
    logged_in_client.post('/projects/new', data={
        'title': 'Mzansi Eats',
        'description': 'A food delivery app for South Africa',
        'stage': 'Prototype',
        'support_required': 'Frontend help'
    })
    response = logged_in_client.get('/')
    assert response.status_code == 200
    assert b'Mzansi Eats' in response.data


def test_project_detail_page(logged_in_client):
    logged_in_client.post('/projects/new', data={
        'title': 'Mzansi Eats',
        'description': 'A food delivery app for South Africa',
        'stage': 'Prototype',
        'support_required': 'Frontend help'
    })
    response = logged_in_client.get('/projects/1')
    assert response.status_code == 200
    assert b'Mzansi Eats' in response.data


def test_project_not_found(logged_in_client):
    response = logged_in_client.get('/projects/999')
    assert response.status_code == 404
