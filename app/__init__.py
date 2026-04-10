from flask import Flask
from config import config
from app.extensions import db, login_manager


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)

    from app.models import User, Project, Comment, Milestone, CollaborationRequest

    from app.routes.auth import auth_bp
    from app.routes.feed import feed_bp
    from app.routes.projects import projects_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(feed_bp)
    app.register_blueprint(projects_bp)

    with app.app_context():
        db.create_all()

    return app
