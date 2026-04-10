from flask import Blueprint, render_template
from app.services.project_service import get_active_projects

feed_bp = Blueprint('feed', __name__)


@feed_bp.route('/')
def index():
    projects = get_active_projects()
    return render_template('feed/index.html', projects=projects)
