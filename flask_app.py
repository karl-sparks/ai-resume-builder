"""
This module contains the main application file for the AI Resume Builder Flask app.
It initializes the Flask app, sets up the database, and configures the login manager.
"""

import os
from dotenv import load_dotenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

from flask_login import LoginManager

from src.sparks_ai import SparksAI
from src.utils import read_input

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
sai = SparksAI()


def create_app():
    """
    Creates and returns the Flask app instance.

    Returns:
        app (Flask): The Flask app instance.
    """
    app = Flask(__name__)

    load_dotenv()

    app.secret_key = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

    inputs_dict = read_input(os.getenv("INPUT_FILE_PATH"))

    template_str = inputs_dict["template"]
    context = inputs_dict["context"]
    convo_history = inputs_dict["convo_history"]

    sai.generate_model(
        model_engine=os.getenv("LLM_MODEL_NAME"),
        prompt_template=template_str,
        context=context,
        convo_history=convo_history,
    )

    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    return app
