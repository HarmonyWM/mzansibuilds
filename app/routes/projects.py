from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from app.services.project_service import create_project, get_project_by_id

projects_bp = Blueprint('projects', __name__)


@projects_bp.route('/projects/new', methods=['GET', 'POST'])
@login_required
def new_project():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        stage = request.form.get('stage', '').strip()
        support_required = request.form.get('support_required', '').strip()

        if not title or not description:
            flash('Title and description are required.')
            return render_template('projects/new.html')

        project = create_project(current_user.id, title, description, stage, support_required)
        return redirect(url_for('projects.detail', project_id=project.id))

    return render_template('projects/new.html')


@projects_bp.route('/projects/<int:project_id>')
def detail(project_id):
    project = get_project_by_id(project_id)
    if not project:
        abort(404)
    return render_template('projects/detail.html', project=project)
