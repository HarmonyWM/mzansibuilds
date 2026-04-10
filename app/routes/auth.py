from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from app.services.auth_service import register_user, get_user_by_email

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not name or not email or not password:
            flash('All fields are required.')
            return render_template('auth/register.html')

        user, error = register_user(name, email, password)
        if error:
            flash(error)
            return render_template('auth/register.html')

        login_user(user)
        return redirect(url_for('feed.index'))

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        user = get_user_by_email(email)
        if not user or not user.check_password(password):
            flash('Invalid email or password.')
            return render_template('auth/login.html')

        login_user(user)
        return redirect(url_for('feed.index'))

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
