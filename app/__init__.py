from flask import Flask
from config import config

from app.routes.main import bp as main
from app.routes.client import bp as client_page
from app.routes.client_edit import bp as client_edit
from app.routes.login import bp as login

from app.extensions import db, migrate
from app.extensions import login_manager

def create_app():
    app = Flask(__name__)

    app.config.update(config)
    db.init_app(app)
    migrate.init_app (app, db)
    login_manager.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(client_page)
    app.register_blueprint(client_edit)
    app.register_blueprint(login)

    app.config ['TEMPLATES_AUTO_RELOAD'] = True
    return app