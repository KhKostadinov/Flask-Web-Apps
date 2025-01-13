from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from lib.config import Config
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'user_routes.login'
login_manager.login_message_category = 'info'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from lib.project_routing import project_routes
    from lib.task_routing import task_routes
    from lib.resource_routing import resource_routes
    from lib.user_routing import user_routes
    app.register_blueprint(project_routes)
    app.register_blueprint(task_routes)
    app.register_blueprint(resource_routes)
    app.register_blueprint(user_routes)
    return app

