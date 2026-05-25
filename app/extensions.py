from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


db = SQLAlchemy()
migrate = Migrate()

login_manager = LoginManager()
login_manager.login_view = 'login.login'

@login_manager.user_loader
def load_user(client_id):
    from app.models import User
    User.query.get(int(client_id))
    return db.session.get(User, int(client_id))
