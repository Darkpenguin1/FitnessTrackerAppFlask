from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
    
class ProductionConfig(Config):
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    conn_str = os.environ['AZURE_POSTGRESQL_CONNECTIONSTRING']
    conn_str_params = {pair.split('=')[0]: pair.split('=')[1] for pair in conn_str.split(' ')}

    DATABASE_URI = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
        dbuser=conn_str_params['user'],
        dbpass=conn_str_params['password'],
        dbhost=conn_str_params['host'],
        dbname=conn_str_params['dbname']
    )
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 20,
        'max_overflow': 0
    }