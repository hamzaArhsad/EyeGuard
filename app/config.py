import os
from datetime import timedelta

class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Secret key for session management
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    
    # JWT configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-jwt-secret-key-here')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # Other configurations
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    
    # Configure flagged incidents directory
    FLAGED_INCIDENTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'flaged_incidents')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Ensure the directory exists
    @staticmethod
    def init_flaged_incidents_dir():
        if not os.path.exists(Config.FLAGED_INCIDENTS_DIR):
            os.makedirs(Config.FLAGED_INCIDENTS_DIR) 