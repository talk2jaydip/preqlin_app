import os

# Get the absolute path of the current directory
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """
    Base configuration class with common settings.
    """
    
    # Define the database URI with a default value (SQLite)
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///data/test.db")
    
    # Define the secret key for the application
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        'AWESOME_SECRETE'
    )
    
    # Define the JWT secret key
    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        'AWESOME_JWT_SECRETE'
    )
    
    # Enable exception propagation for better error handling
    PROPAGATE_EXCEPTIONS = True
    
    # Enable JWT token blacklist
    JWT_BLACKLIST_ENABLED = True
    
    # Specify which JWT token types to check for blacklist
    JWT_BLACKLIST_TOKEN_CHECKS = [
        "access",
        "refresh",
    ]

class ProdConfig(Config):
    """
    Production configuration with optimizations and disabled tracking of modifications.
    """
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):
    """
    Development configuration with debugging enabled.
    """
    
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class TestConfig(Config):
    """
    Testing configuration with debugging enabled and a predefined test database URI.
    """
    
    FLASK_ENV = "test"
    DEBUG = True
    SECRET_KEY = "jaydip"
    JWT_SECRET_KEY = "jaydip"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///E:/preqlin/app/temp.db"
