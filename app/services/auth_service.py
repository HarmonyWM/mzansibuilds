import re
from app.extensions import db
from app.models.user import User

EMAIL_REGEX = re.compile(r'^[^@]+@[^@]+\.[^@]+$')


def register_user(name, email, password):
    """Register a new user after validating email format and password length.

    Returns a tuple of (user, error). On success, error is None.
    On failure, user is None and error contains the reason.
    """
    if not EMAIL_REGEX.match(email):
        return None, 'Invalid email address.'
    if len(password) < 8:
        return None, 'Password must be at least 8 characters.'
    if User.query.filter_by(email=email).first():
        return None, 'Email already registered'
    user = User(name=name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user, None


def get_user_by_email(email):
    """Retrieve a user by their email address. Returns None if not found."""
    return User.query.filter_by(email=email).first()
