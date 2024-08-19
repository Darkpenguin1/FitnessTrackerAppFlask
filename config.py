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

    conn_str = os.getenv('AZURE_POSTGRESQL_CONNECTIONSTRING')
    if conn_str:
        try:
            # Parsing the connection string
            conn_str_params = {}
            for pair in conn_str.split(';'):
                if '=' in pair:
                    key, value = pair.split('=', 1)
                    conn_str_params[key.strip()] = value.strip()

            DATABASE_URI = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
                dbuser=conn_str_params.get('User Id'),
                dbpass=conn_str_params.get('Password'),
                dbhost=conn_str_params.get('Server'),
                dbname=conn_str_params.get('Database')
            )
            SQLALCHEMY_DATABASE_URI = DATABASE_URI
        except Exception as e:
            raise ValueError(f"Error parsing AZURE_POSTGRESQL_CONNECTIONSTRING: {e}")
    else:
        raise ValueError("AZURE_POSTGRESQL_CONNECTIONSTRING environment variable not set")

    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 20,
        'max_overflow': 0
    }