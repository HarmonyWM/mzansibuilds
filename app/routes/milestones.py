from flask import Blueprint, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from app.services.milestone_service import add_milestone, complete_project
from app.services.project_service import get_project_by_id

milestones_bp = Blueprint('milestones', __name__)


@milestones_bp.route('/projects/<int:project_id>/milestones', methods=['POST'])
@login_required
def new_milestone(project_id):
    project = get_project_by_id(project_id)
    if not project:
        abort(404)
    if project.user_id != current_user.id:
        flash('Only the project owner can add milestones.')
        return redirect(url_for('projects.detail', project_id=project_id))

    content = request.form.get('content', '').strip()
    if not content:
        flash('Milestone content is required.')
        return redirect(url_for('projects.detail', project_id=project_id))

    add_milestone(project_id, content)
    return redirect(url_for('projects.detail', project_id=project_id))


@milestones_bp.route('/projects/<int:project_id>/complete', methods=['POST'])
@login_required
def mark_complete(project_id):
    project = get_project_by_id(project_id)
    if not project:
        abort(404)
    if project.user_id != current_user.id:
        flash('Only the project owner can mark it as complete.')
        return redirect(url_for('projects.detail', project_id=project_id))

    complete_project(project_id)
    return redirect(url_for('celebration.index'))
