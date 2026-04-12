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


def test_celebration_wall_loads(client):
    response = client.get('/celebration')
    assert response.status_code == 200


def test_celebration_wall_empty_state(client):
    response = client.get('/celebration')
    assert response.status_code == 200
