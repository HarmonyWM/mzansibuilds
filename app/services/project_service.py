from app.extensions import db
from app.models.project import Project
from app.models.comment import Comment
from app.models.collaboration import CollaborationRequest


def create_project(user_id, title, description, stage, support_required):
    """Create and persist a new project owned by the given user."""
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
    """Retrieve a project by its ID. Returns None if not found."""
    return db.session.get(Project, project_id)


def get_active_projects():
    """Return all active projects ordered by most recently created."""
    return Project.query.filter_by(status='active').order_by(Project.created_at.desc()).all()


def add_comment(project_id, user_id, content):
    """Add a comment to a project on behalf of a user."""
    comment = Comment(project_id=project_id, user_id=user_id, content=content)
    db.session.add(comment)
    db.session.commit()
    return comment


def add_collaboration_request(project_id, user_id, message):
    """Submit a collaboration request for a project on behalf of a user."""
    collab = CollaborationRequest(project_id=project_id, user_id=user_id, message=message)
    db.session.add(collab)
    db.session.commit()
    return collab
