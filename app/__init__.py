from flask import Flask
from config import config

from app.routes.main import bp as main
from app.routes.client import bp as client_page
from app.routes.client_edit import bp as client_edit

from app.extensions import db, migrate

def create_app():
    app = Flask(__name__)

    app.config.update(config)
    db.init_app(app)
    migrate.init_app (app, db)

    app.register_blueprint(main)
    app.register_blueprint(client_page)
    app.register_blueprint(client_edit)

    app.config ['TEMPLATES_AUTO_RELOAD'] = True
    return app