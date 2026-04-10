from app.extensions import db
from app.models.user import User


def register_user(name, email, password):
    if User.query.filter_by(email=email).first():
        return None, 'Email already registered'
    user = User(name=name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user, None


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()
