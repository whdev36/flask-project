from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, current_user, logout_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            flash('Welcome back, {}!'.format(user.first_name), 'success')
            login_user(user, remember=True)
            return redirect(url_for('views.index'))
        elif user:
            flash('Incorrect password. Please try again.', 'warning')
        else:
            flash('The email you entered does not exist. Please register first.', 'warning')

    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        first_name = request.form.get('first-name', '').strip()
        last_name = request.form.get('last-name', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm-password', '').strip()

        if len(email) < 5 or '@' not in email:
            flash('Please enter a valid email address.', 'warning')
        elif User.query.filter_by(email=email).first():
            flash('Email already exists. Please log in.', 'warning')
        elif len(password) < 6:
            flash('Password must be at least 6 characters long.', 'warning')
        elif password != confirm_password:
            flash('Passwords do not match. Please try again.', 'warning')
        else:
            new_user = User(
                email=email, 
                first_name=first_name,
                last_name=last_name,
                password=generate_password_hash(password)
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Your account has been created successfully!', 'success')
            return redirect(url_for('views.index'))

    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))