from dotenv import load_dotenv
import os
import psycopg2


load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv('POSTGRESQLDB_USER')}:{os.getenv('POSTGRESQLDB_PASSWORD')}"
        f"@{os.getenv('POSTGRESQLDB_SERVER')}:{os.getenv('POSTGRESQLDB_PORT')}/{os.getenv('POSTGRESQLDB_NAME')}"
    )

    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 20,
        'max_overflow': 0
    }
    
    