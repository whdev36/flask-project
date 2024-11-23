from flask import (Flask, render_template, request, current_app,
				make_response, redirect, abort, url_for, session,
				flash)
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from uuid import uuid4
import os
from flask_mail import Mail, Message

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

db =SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

class NameForm(FlaskForm):
	name = StringField('What\'s your name?', validators=[DataRequired()])
	submit = SubmitField('Submit')

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	users = db.relationship('User', backref='role')

	def __repr__(self):
		return '<Role %r>' % self.name

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

	def __repr__(self):
		return '<User %r>' % self.username

@app.route('/', methods=['POST', 'GET'])
def index():
	form = NameForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.name.data).first()
		if user is None:
			user = User(username=form.name.data)
			db.session.add(user)
			db.session.commit()
			session['know'] = False
		else:
			session['know'] =True
		session['name'] = form.name.data
		return redirect(url_for('index'))
	return render_template('index.html',
		form=form, name=session.get('name'),
		know=session.get('know', False))

@app.route('/user/<name>')
def get_user(name):
	return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500

@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'user':  User, 'role': Role}

if __name__ == '__main__':
	app.run(debug=True)