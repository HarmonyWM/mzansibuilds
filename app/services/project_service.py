from app.extensions import db
from app.models.project import Project
from app.models.comment import Comment
from app.models.collaboration import CollaborationRequest


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
    return db.session.get(Project, project_id)


def get_active_projects():
    return Project.query.filter_by(status='active').order_by(Project.created_at.desc()).all()


def add_comment(project_id, user_id, content):
    comment = Comment(project_id=project_id, user_id=user_id, content=content)
    db.session.add(comment)
    db.session.commit()
    return comment


def add_collaboration_request(project_id, user_id, message):
    collab = CollaborationRequest(project_id=project_id, user_id=user_id, message=message)
    db.session.add(collab)
    db.session.commit()
    return collab
