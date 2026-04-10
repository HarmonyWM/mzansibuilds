from flask import Flask
from config import config
from app.extensions import db, login_manager


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)

    from app.models import User, Project, Comment, Milestone, CollaborationRequest

    with app.app_context():
        db.create_all()

    return app
