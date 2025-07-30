"""
Configuration settings for the File Merger application.
"""

import os
from pathlib import Path

# Application settings
APP_NAME = "File Merger"
APP_VERSION = "1.0.0"
APP_AUTHOR = "File Merger Team"

# File settings
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB
MAX_FILES_PER_MERGE = 50
SUPPORTED_PDF_EXTENSIONS = [".pdf"]
SUPPORTED_EXCEL_EXTENSIONS = [".xlsx", ".xls", ".xlsm"]

# Default paths
DEFAULT_OUTPUT_DIR = str(Path.home() / "Desktop")
LOG_FILE = "file_merger.log"
CONFIG_DIR = str(Path.home() / ".file_merger")

# GUI settings
WINDOW_MIN_WIDTH = 600
WINDOW_MIN_HEIGHT = 500
WINDOW_DEFAULT_WIDTH = 800
WINDOW_DEFAULT_HEIGHT = 700

# CLI settings
CLI_BATCH_SIZE = 10
CLI_PROGRESS_UPDATE_INTERVAL = 1.0

# Performance settings
MEMORY_LIMIT = 1024 * 1024 * 1024  # 1GB
TEMP_DIR = None  # Use system temp directory

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
LOG_BACKUP_COUNT = 3

# PDF specific settings
PDF_DEFAULT_ADD_BOOKMARKS = True
PDF_PRESERVE_METADATA = True
PDF_OPTIMIZE_OUTPUT = False

# Excel specific settings
EXCEL_DEFAULT_SHEET_PREFIX = ""
EXCEL_PRESERVE_FORMULAS = True
EXCEL_PRESERVE_FORMATTING = True

# Create config directory if it doesn't exist
os.makedirs(CONFIG_DIR, exist_ok=True)
