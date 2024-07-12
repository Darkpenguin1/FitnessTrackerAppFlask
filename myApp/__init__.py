from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from config import Config
from dotenv import load_dotenv
import os


db = SQLAlchemy()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(Config)
    app.permanent_session_lifetime = timedelta(hours=5)
    
    db.init_app(app)

    

    with app.app_context():
        from myApp.blueprints.user import routes  # Import routes here to avoid circular imports
        from myApp.blueprints.user.routes import user_bp
        app.register_blueprint(user_bp, url_prefix="/")
        return app
