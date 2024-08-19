from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    conn_str = os.getenv('AZURE_POSTGRESQL_CONNECTIONSTRING')
    conn_str_params = {pair.split('=')[0].strip(): pair.split('=')[1].strip() for pair in conn_str.split(';') if '=' in pair}
    
    DATABASE_URI = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
        dbuser=conn_str_params.get('User Id'),
        dbpass=conn_str_params.get('Password'),
        dbhost=conn_str_params.get('Server'),
        dbname=conn_str_params.get('Database')
    )

    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 20,
        'max_overflow': 0
    }
    
    