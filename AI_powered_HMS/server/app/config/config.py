import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'kaire-health-super-secret-jwt-key-2026-enterprise')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'kaire-jwt-secure-token-2026')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(os.getenv('JWT_EXPIRES_HOURS', 12)))

    # MySQL / SQLite Dual-Support Database URI
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'rootpassword')
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_PORT = os.getenv('MYSQL_PORT', '3306')
    MYSQL_DB = os.getenv('MYSQL_DB', 'kaire_health')

    # If DATABASE_URL is set directly in .env or Render/Railway
    DATABASE_URL = os.getenv('DATABASE_URL')

    if DATABASE_URL:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    elif os.getenv('USE_MYSQL', 'false').lower() == 'true':
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    else:
        # Default SQLite database for immediate zero-config local run
        basedir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        db_path = os.path.join(basedir, 'kaire_health.db')
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 280,
    } if 'mysql' in SQLALCHEMY_DATABASE_URI else {}

    # ML models directory
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
    ML_DIR = os.path.join(BASE_DIR, 'ml')
    
    CORS_HEADERS = 'Content-Type'
    SWAGGER = {
        'title': 'KAIre Health REST API',
        'uiversion': 3,
        'description': 'RESTful API and ML Diagnostic Engine for KAIre Hospital Management System'
    }

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
