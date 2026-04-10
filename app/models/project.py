from app.extensions import db
from datetime import datetime


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    stage = db.Column(db.String(50))
    support_required = db.Column(db.String(150))
    status = db.Column(db.String(50), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    comments = db.relationship('Comment', backref='project', lazy=True)
    milestones = db.relationship('Milestone', backref='project', lazy=True)
    collaboration_requests = db.relationship('CollaborationRequest', backref='project', lazy=True)
