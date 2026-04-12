from flask import Blueprint, render_template
from app.services.milestone_service import get_completed_projects

celebration_bp = Blueprint('celebration', __name__)


@celebration_bp.route('/celebration')
def index():
    projects = get_completed_projects()
    return render_template('celebration/index.html', projects=projects)
