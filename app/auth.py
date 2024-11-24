from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pass
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email', '')
        first_name = request.form.get('first-name', '')
        last_name = request.form.get('last-name', '')
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm-password', '')

        if password != confirm_password:
            flash('Password don\'t match.', 'warning')
        else:
            new_user = User(email=email, first_name=first_name,
                            last_name=last_name,
                            password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', 'success')
            return redirect(url_for('views.index'))

    return render_template('register.html')

@auth.route('/logout')
def logout():
    return '<p>Logout</p>'