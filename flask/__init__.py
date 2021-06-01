from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ, path

db = SQLAlchemy()


def init_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    # app.config.from_object('config.Config')

    # General Config
    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    db.init_app(app)

    with app.app_context():
        # from . import routes  # Import routes
        import routes
        db.create_all()  # Create sql tables for our data models

        return app