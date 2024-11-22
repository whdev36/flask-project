from flask import (Flask, render_template, request, current_app,
				make_response, redirect, abort, url_for)
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from uuid import uuid4

# Configure app
app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')
app.config['SECRET_KEY'] = 'dfdfdf'

class NameForm(FlaskForm):
	name = StringField('What\'s your name?', validators=[DataRequired()])
	submit = SubmitField('Submit')

@app.route('/', methods=['POST', 'GET'])
def index():
	name = None
	form = NameForm()
	if form.validate_on_submit():
		name = form.name.data
		form.name.data = ''
	return render_template('index.html', form=form, name=name)

@app.route('/user/<name>')
def get_user(name):
	return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500

if __name__ == '__main__':
	app.run(debug=True)