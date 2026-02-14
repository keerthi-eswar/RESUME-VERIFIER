"""
Logging Configuration Module
Sets up logging for the application
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from backend.config import config


def setup_logger(name: str, log_level: str = None) -> logging.Logger:
    """
    Setup logger with console and file handlers

    Args:
        name: Logger name (usually __name__)
        log_level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Configured logger instance
    """
    if log_level is None:
        log_level = config.LOG_LEVEL

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level))

    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(config.LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level))

    # File handler with rotation
    file_handler = RotatingFileHandler(
        config.LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(getattr(logging, log_level))

    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to logger
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger


# Create default logger
logger = setup_logger(__name__)
