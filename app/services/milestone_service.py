from app.extensions import db
from app.models.milestone import Milestone
from app.models.project import Project


def add_milestone(project_id, content):
    milestone = Milestone(project_id=project_id, content=content)
    db.session.add(milestone)
    db.session.commit()
    return milestone


def complete_project(project_id):
    project = db.session.get(Project, project_id)
    if project:
        project.status = 'completed'
        db.session.commit()
    return project


def get_completed_projects():
    return Project.query.filter_by(status='completed').order_by(Project.created_at.desc()).all()
