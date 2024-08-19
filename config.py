from dotenv import load_dotenv
import os
import psycopg2


load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    db_name = os.getenv('POSTGRESQLDB_NAME')
    db_server = os.getenv('POSTGRESQLDB_SERVER')
    db_user = os.getenv('POSTGRESQLDB_USER')
    db_password = os.getenv('POSTGRESQLDB_PASSWORD')

    DATABASE_URI = f'postgresql+psycopg2://{db_user}:{db_password}@{db_server}/{db_name}'

    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 20,
        'max_overflow': 0
    }
    
    