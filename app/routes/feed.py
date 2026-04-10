from flask import Blueprint, render_template

feed_bp = Blueprint('feed', __name__)


@feed_bp.route('/')
def index():
    return render_template('feed/index.html')
