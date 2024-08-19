from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from datetime import timedelta
from config import Config, ProductionConfig
from dotenv import load_dotenv
import os
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

db = SQLAlchemy()
migrate = Migrate()
admin = Admin()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    
    if os.getenv('FLASK_ENV') == 'development':
        app.config.from_object(Config)
    else:
        app.config.from_object(ProductionConfig)
    
    
    app.permanent_session_lifetime = timedelta(hours=5)
    
    
    db.init_app(app)
    migrate.init_app(app, db)
    admin.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "user_bp.login"
    login_manager.init_app(app)

    
    from myApp.models import User   # prevents circular imports
    from myApp.models import Exercise

    admin.add_view(ModelView(User, db.session))     ##  Can crud users CANNOT CRUD exercises or the relationship between users and there exercises through admin dashboard YET 
    admin.add_view(ModelView(Exercise, db.session))

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    

    with app.app_context():
        from myApp.blueprints.user import routes  # Import routes here to avoid circular imports
        from myApp.blueprints.user.routes import user_bp
        
        from myApp.blueprints.admin.routes import admin_bp
        from myApp.blueprints.admin import routes
        app.register_blueprint(admin_bp, url_prefix="/admin")
        
        app.register_blueprint(user_bp, url_prefix="/")
        
        return app
