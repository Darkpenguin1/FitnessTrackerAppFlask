from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from config import Config
from dotenv import load_dotenv
import os
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(Config)
    app.permanent_session_lifetime = timedelta(hours=5)
    
    db.init_app(app)
    migrate.init_app(app, db)

    login_manager = LoginManager()
    login_manager.login_view = "user_bp.login"
    login_manager.init_app(app)

    from myApp.models import User   # prevents circular imports

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    

    with app.app_context():
        from myApp.blueprints.user import routes  # Import routes here to avoid circular imports
        from myApp.blueprints.user.routes import user_bp
        app.register_blueprint(user_bp, url_prefix="/")
        return app
