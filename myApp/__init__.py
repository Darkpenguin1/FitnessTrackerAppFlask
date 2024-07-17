from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from config import Config
from dotenv import load_dotenv
import os
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_admin import Admin

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(Config)
    app.permanent_session_lifetime = timedelta(hours=5)
    # Inside create_app function or where you configure your Flask app
    

    db.init_app(app)
    migrate.init_app(app, db)

    login_manager = LoginManager()
    login_manager.login_view = "user_bp.login"
    login_manager.init_app(app)

    
    from myApp.models import User   # prevents circular imports
    """
    admin = Admin(app, 'Admin Panel')
    admin.add_view(User, db.session)
    """

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    

    with app.app_context():
        from myApp.blueprints.user import routes  # Import routes here to avoid circular imports
        from myApp.blueprints.user.routes import user_bp
        """
        from myApp.blueprints.admin.routes import admin_bp
        from myApp.blueprints.admin import routes
        app.register_blueprint(admin_bp, url_prefix="/admin")
        """
        app.register_blueprint(user_bp, url_prefix="/")
        
        return app
