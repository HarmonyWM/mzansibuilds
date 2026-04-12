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


def test_add_milestone_success(project):
    response = project.post('/projects/1/milestones', data={
        'content': 'Finished the login system'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Finished the login system' in response.data


def test_add_milestone_missing_content(project):
    response = project.post('/projects/1/milestones', data={
        'content': ''
    }, follow_redirects=True)
    assert b'required' in response.data


def test_add_milestone_requires_login(client):
    response = client.post('/projects/1/milestones', data={
        'content': 'Finished the login system'
    }, follow_redirects=True)
    assert b'Login' in response.data


def test_milestones_show_on_project_detail(project):
    project.post('/projects/1/milestones', data={
        'content': 'Set up the database'
    })
    response = project.get('/projects/1')
    assert b'Set up the database' in response.data


def test_mark_project_complete(project):
    response = project.post('/projects/1/complete', follow_redirects=True)
    assert response.status_code == 200


def test_mark_project_complete_requires_login(client):
    response = client.post('/projects/1/complete', follow_redirects=True)
    assert b'Login' in response.data


def test_completed_project_appears_on_celebration_wall(project):
    project.post('/projects/1/complete')
    response = project.get('/celebration')
    assert response.status_code == 200
    assert b'Mzansi Eats' in response.data


def test_active_project_not_on_celebration_wall(project):
    response = project.get('/celebration')
    assert b'Mzansi Eats' not in response.data
