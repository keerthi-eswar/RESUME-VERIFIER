"""
File Handler Utility Module
Handles file operations and validation
"""

import os
from typing import List, Tuple
from backend.config import config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class FileHandler:
    """Handles file operations and validation"""

    @staticmethod
    def validate_file(filename: str, file_content: bytes) -> Tuple[bool, str]:
        """
        Validate uploaded file

        Args:
            filename: Original filename
            file_content: File bytes

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check file extension
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext not in config.ALLOWED_EXTENSIONS:
            return False, f"File type {file_ext} not allowed. Use {config.ALLOWED_EXTENSIONS}"

        # Check file size
        file_size = len(file_content)
        if file_size > config.MAX_FILE_SIZE:
            return False, f"File size {file_size} exceeds maximum {config.MAX_FILE_SIZE}"

        if file_size == 0:
            return False, "File is empty"

        return True, ""

    @staticmethod
    def validate_job_description(text: str) -> Tuple[bool, str]:
        """
        Validate job description input

        Args:
            text: Job description text

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not text or not text.strip():
            return False, "Job description cannot be empty"

        if len(text) < 50:
            return False, "Job description too short (minimum 50 characters)"

        if len(text) > 100000:
            return False, "Job description too long (maximum 100,000 characters)"

        return True, ""

    @staticmethod
    def get_file_info(filename: str) -> dict:
        """
        Extract file information

        Args:
            filename: Filename

        Returns:
            Dictionary with file info
        """
        name, ext = os.path.splitext(filename)
        return {
            "filename": filename,
            "name": name,
            "extension": ext.lower(),
            "is_pdf": ext.lower() == ".pdf",
            "is_docx": ext.lower() == ".docx",
        }

    @staticmethod
    def save_temp_file(filename: str, content: bytes, temp_dir: str = "./temp") -> str:
        """
        Save file temporarily

        Args:
            filename: Filename
            content: File content bytes
            temp_dir: Temporary directory path

        Returns:
            Path to saved file
        """
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        filepath = os.path.join(temp_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(content)

        logger.info(f"Saved temp file: {filepath}")
        return filepath

    @staticmethod
    def delete_temp_file(filepath: str) -> bool:
        """
        Delete temporary file

        Args:
            filepath: Path to file

        Returns:
            Success status
        """
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.info(f"Deleted temp file: {filepath}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting file {filepath}: {str(e)}")
            return False

    @staticmethod
    def cleanup_temp_dir(temp_dir: str = "./temp") -> None:
        """
        Cleanup all temporary files

        Args:
            temp_dir: Temporary directory path
        """
        try:
            if os.path.exists(temp_dir):
                for file in os.listdir(temp_dir):
                    filepath = os.path.join(temp_dir, file)
                    if os.path.isfile(filepath):
                        os.remove(filepath)
                logger.info(f"Cleaned up temp directory: {temp_dir}")
        except Exception as e:
            logger.error(f"Error cleaning temp directory: {str(e)}")
