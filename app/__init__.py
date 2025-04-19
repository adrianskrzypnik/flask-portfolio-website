from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv
import os


db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app():
    load_dotenv()

    app = Flask(__name__)

    app.config.from_object('app.config.Config')

    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.projects import projects_bp
    from app.routes.admin import admin_bp
    from app.routes.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    from app.models import user, project, skill, message, about

    @login_manager.user_loader
    def load_user(user_id):
        return user.User.query.get(int(user_id))

    from app.commands import init_db_command
    app.cli.add_command(init_db_command)

    return app