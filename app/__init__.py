from flask import Flask
import os

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'CREATE_YOUR_SECRET_KEY'

    from .views import views
    from .auth import auth

    app.register_blueprint(views)
    app.register_blueprint(auth)

    return app