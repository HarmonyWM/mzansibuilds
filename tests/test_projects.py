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


@pytest.fixture
def project(logged_in_client):
    logged_in_client.post('/projects/new', data={
        'title': 'Mzansi Eats',
        'description': 'A food delivery app for South Africa',
        'stage': 'Prototype',
        'support_required': 'Frontend help'
    })
    return logged_in_client


def test_add_comment_success(project):
    response = project.post('/projects/1/comment', data={
        'content': 'This looks amazing!'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'This looks amazing!' in response.data


def test_add_comment_missing_content(project):
    response = project.post('/projects/1/comment', data={
        'content': ''
    }, follow_redirects=True)
    assert b'required' in response.data


def test_add_comment_requires_login(client):
    response = client.post('/projects/1/comment', data={
        'content': 'This looks amazing!'
    }, follow_redirects=True)
    assert b'Login' in response.data


def test_add_collaboration_request_success(project):
    response = project.post('/projects/1/collaborate', data={
        'message': 'I can help with the frontend!'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'I can help with the frontend!' in response.data


def test_add_collaboration_request_missing_message(project):
    response = project.post('/projects/1/collaborate', data={
        'message': ''
    }, follow_redirects=True)
    assert b'required' in response.data


def test_add_collaboration_request_requires_login(client):
    response = client.post('/projects/1/collaborate', data={
        'message': 'I can help!'
    }, follow_redirects=True)
    assert b'Login' in response.data


def test_comments_show_on_project_detail(project):
    project.post('/projects/1/comment', data={
        'content': 'Great project!'
    })
    response = project.get('/projects/1')
    assert b'Great project!' in response.data


def test_collaboration_requests_show_on_project_detail(project):
    project.post('/projects/1/collaborate', data={
        'message': 'I want to help!'
    })
    response = project.get('/projects/1')
    assert b'I want to help!' in response.data
