from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = 'website.db'

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'CREATE_YOUR_SECRET_KEY'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views)
    app.register_blueprint(auth)

    if not os.path.exists(DB_NAME):
        with app.app_context():
            db.create_all()
        print(f'{DB_NAME} created successfully!')


    return app
