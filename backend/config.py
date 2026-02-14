"""
Configuration Module
Manages environment variables and settings
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""

    # API Settings
    API_TITLE = "Resume Screening API"
    API_VERSION = "1.0.0"
    API_DESCRIPTION = "AI-powered resume screening using semantic embeddings"
    DEBUG = os.getenv("DEBUG", "False") == "True"

    # Server Settings
    PORT = int(os.getenv("PORT", 8000))
    HOST = os.getenv("HOST", "0.0.0.0")

    # Embedding Settings
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

    # Azure Settings (for production deployment)
    AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY", "")
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "")

    # File Upload Settings
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 10 * 1024 * 1024))  # 10MB
    ALLOWED_EXTENSIONS = {".pdf", ".docx"}

    # Similarity Threshold Settings
    MIN_SIMILARITY_THRESHOLD = float(os.getenv("MIN_SIMILARITY_THRESHOLD", 0.3))
    HIGH_RELEVANCE_THRESHOLD = float(os.getenv("HIGH_RELEVANCE_THRESHOLD", 0.8))

    # Logging Settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/resume_screening.log")

    # CORS Settings
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

    # Database Settings (for future use)
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///resume_screening.db")


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    LOG_LEVEL = "INFO"


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    DATABASE_URL = "sqlite:///:memory:"
    LOG_LEVEL = "DEBUG"


# Get config based on environment
ENV = os.getenv("ENVIRONMENT", "development")

if ENV == "production":
    config = ProductionConfig()
elif ENV == "testing":
    config = TestingConfig()
else:
    config = DevelopmentConfig()
