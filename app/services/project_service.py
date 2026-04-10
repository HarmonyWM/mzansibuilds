from app.extensions import db
from app.models.project import Project


def create_project(user_id, title, description, stage, support_required):
    project = Project(
        user_id=user_id,
        title=title,
        description=description,
        stage=stage,
        support_required=support_required
    )
    db.session.add(project)
    db.session.commit()
    return project


def get_project_by_id(project_id):
    return Project.query.get(project_id)


def get_active_projects():
    return Project.query.filter_by(status='active').order_by(Project.created_at.desc()).all()
