import os
from pathlib import Path

# Base directory of the application
BASE_DIR = Path(__file__).resolve().parent

class Config:
    """Base application configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-jalaraksha-local-only')
    
    # Instance path for SQLite DB and private uploads
    INSTANCE_PATH = BASE_DIR / 'instance'
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        f"sqlite:///{INSTANCE_PATH / 'jalaraksha.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Uploads (Private, outside static/)
    UPLOAD_FOLDER = INSTANCE_PATH / 'uploads'
    MAX_CONTENT_LENGTH = 3 * 1024 * 1024  # 3 MB limit
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}
    
    # Security & Sessions
    WTF_CSRF_ENABLED = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'

class TestingConfig(Config):
    """Testing configuration with in-memory SQLite and disabled CSRF for test convenience."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    UPLOAD_FOLDER = BASE_DIR / 'instance' / 'test_uploads'
