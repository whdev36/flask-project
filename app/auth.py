from flask import Blueprint, render_template, request, flash

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
            flash('Account created!', 'success')

    return render_template('register.html')

@auth.route('/logout')
def logout():
    return '<p>Logout</p>'