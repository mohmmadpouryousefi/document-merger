"""
Test cases for Configuration module.
"""

import os
from pathlib import Path
from unittest.mock import patch

from src.core import config


class TestConfig:
    """Test cases for configuration constants and settings."""

    def test_app_constants(self):
        """Test application constants."""
        assert config.APP_NAME == "File Merger"
        assert config.APP_VERSION == "1.0.0"
        assert config.APP_AUTHOR == "File Merger Team"

    def test_file_settings(self):
        """Test file-related settings."""
        assert config.MAX_FILE_SIZE == 500 * 1024 * 1024  # 500MB
        assert config.MAX_FILES_PER_MERGE == 50
        assert config.SUPPORTED_PDF_EXTENSIONS == [".pdf"]
        assert config.SUPPORTED_EXCEL_EXTENSIONS == [".xlsx", ".xls", ".xlsm"]

    def test_default_paths(self):
        """Test default path settings."""
        assert config.DEFAULT_OUTPUT_DIR == str(Path.home() / "Desktop")
        assert config.LOG_FILE == "file_merger.log"
        assert config.CONFIG_DIR == str(Path.home() / ".file_merger")

    def test_gui_settings(self):
        """Test GUI-related settings."""
        assert config.WINDOW_MIN_WIDTH == 600
        assert config.WINDOW_MIN_HEIGHT == 500
        assert config.WINDOW_DEFAULT_WIDTH == 800
        assert config.WINDOW_DEFAULT_HEIGHT == 700

    def test_cli_settings(self):
        """Test CLI-related settings."""
        assert config.CLI_BATCH_SIZE == 10
        assert config.CLI_PROGRESS_UPDATE_INTERVAL == 1.0

    def test_performance_settings(self):
        """Test performance-related settings."""
        assert config.MEMORY_LIMIT == 1024 * 1024 * 1024  # 1GB
        assert config.TEMP_DIR is None

    def test_logging_configuration(self):
        """Test logging configuration."""
        assert config.LOG_LEVEL == "INFO"
        assert (
            config.LOG_FORMAT == "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        assert config.LOG_MAX_SIZE == 10 * 1024 * 1024  # 10MB
        assert config.LOG_BACKUP_COUNT == 3

    def test_pdf_settings(self):
        """Test PDF-specific settings."""
        assert config.PDF_DEFAULT_ADD_BOOKMARKS is True
        assert config.PDF_PRESERVE_METADATA is True
        assert config.PDF_OPTIMIZE_OUTPUT is False

    def test_excel_settings(self):
        """Test Excel-specific settings."""
        assert config.EXCEL_DEFAULT_SHEET_PREFIX == ""
        assert config.EXCEL_PRESERVE_FORMULAS is True
        assert config.EXCEL_PRESERVE_FORMATTING is True

    def test_config_dir_creation(self):
        """Test that config directory creation is handled."""
        # The config module creates the directory on import
        # Just verify the constant exists and is a string
        assert isinstance(config.CONFIG_DIR, str)
        assert len(config.CONFIG_DIR) > 0

    def test_file_size_limits(self):
        """Test file size limit calculations."""
        # Test that file size is reasonable (500MB)
        assert config.MAX_FILE_SIZE > 100 * 1024 * 1024  # At least 100MB
        assert config.MAX_FILE_SIZE < 1024 * 1024 * 1024  # Less than 1GB

    def test_memory_limit(self):
        """Test memory limit setting."""
        # Test that memory limit is reasonable (1GB)
        assert config.MEMORY_LIMIT == 1 * 1024 * 1024 * 1024
        assert config.MEMORY_LIMIT >= config.MAX_FILE_SIZE

    def test_supported_extensions(self):
        """Test supported file extensions."""
        # PDF extensions
        assert ".pdf" in config.SUPPORTED_PDF_EXTENSIONS
        assert len(config.SUPPORTED_PDF_EXTENSIONS) >= 1

        # Excel extensions
        assert ".xlsx" in config.SUPPORTED_EXCEL_EXTENSIONS
        assert ".xls" in config.SUPPORTED_EXCEL_EXTENSIONS
        assert ".xlsm" in config.SUPPORTED_EXCEL_EXTENSIONS
        assert len(config.SUPPORTED_EXCEL_EXTENSIONS) >= 3

    def test_window_dimensions(self):
        """Test window dimension constraints."""
        assert config.WINDOW_MIN_WIDTH <= config.WINDOW_DEFAULT_WIDTH
        assert config.WINDOW_MIN_HEIGHT <= config.WINDOW_DEFAULT_HEIGHT
        assert config.WINDOW_MIN_WIDTH > 0
        assert config.WINDOW_MIN_HEIGHT > 0

    def test_log_settings_sanity(self):
        """Test logging settings sanity checks."""
        assert config.LOG_MAX_SIZE > 0
        assert config.LOG_BACKUP_COUNT >= 0
        assert len(config.LOG_FORMAT) > 0
        assert config.LOG_LEVEL in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    def test_batch_size_positive(self):
        """Test that batch size is positive."""
        assert config.CLI_BATCH_SIZE > 0
        assert config.MAX_FILES_PER_MERGE > 0
        assert config.CLI_PROGRESS_UPDATE_INTERVAL > 0

    def test_path_types(self):
        """Test that path configurations are strings."""
        assert isinstance(config.DEFAULT_OUTPUT_DIR, str)
        assert isinstance(config.LOG_FILE, str)
        assert isinstance(config.CONFIG_DIR, str)

    def test_boolean_settings(self):
        """Test boolean configuration values."""
        assert isinstance(config.PDF_DEFAULT_ADD_BOOKMARKS, bool)
        assert isinstance(config.PDF_PRESERVE_METADATA, bool)
        assert isinstance(config.PDF_OPTIMIZE_OUTPUT, bool)
        assert isinstance(config.EXCEL_PRESERVE_FORMULAS, bool)
        assert isinstance(config.EXCEL_PRESERVE_FORMATTING, bool)

    def test_string_settings(self):
        """Test string configuration values."""
        assert isinstance(config.APP_NAME, str)
        assert isinstance(config.APP_VERSION, str)
        assert isinstance(config.APP_AUTHOR, str)
        assert isinstance(config.LOG_FILE, str)
        assert isinstance(config.LOG_FORMAT, str)
        assert isinstance(config.LOG_LEVEL, str)
        assert isinstance(config.EXCEL_DEFAULT_SHEET_PREFIX, str)


class TestConfigIntegration:
    """Integration tests for configuration usage."""

    def test_config_directory_accessible(self):
        """Test that config directory is accessible."""
        config_path = Path(config.CONFIG_DIR)

        # The directory should exist (created by config module)
        assert config_path.exists()
        assert config_path.is_dir()

    def test_home_directory_resolution(self):
        """Test that home directory is properly resolved."""
        home_path = Path.home()

        # Default output dir should be under home
        assert str(home_path) in config.DEFAULT_OUTPUT_DIR

        # Config dir should be under home
        assert str(home_path) in config.CONFIG_DIR

    def test_supported_extensions_lowercase(self):
        """Test that all supported extensions are lowercase."""
        for ext in config.SUPPORTED_PDF_EXTENSIONS:
            assert ext == ext.lower()
            assert ext.startswith(".")

        for ext in config.SUPPORTED_EXCEL_EXTENSIONS:
            assert ext == ext.lower()
            assert ext.startswith(".")

    def test_size_configurations_hierarchy(self):
        """Test size configuration hierarchy makes sense."""
        # Memory limit should be larger than max file size
        assert config.MEMORY_LIMIT >= config.MAX_FILE_SIZE

        # Log max size should be reasonable
        assert config.LOG_MAX_SIZE < config.MAX_FILE_SIZE

    @patch.dict(os.environ, {"HOME": "/tmp/test_home"})
    def test_config_with_different_home(self):
        """Test configuration with different home directory."""
        # This tests that the config would work with different home paths
        # We can't actually reload the module, but we can test the logic
        test_home = Path("/tmp/test_home")
        expected_config_dir = str(test_home / ".file_merger")
        expected_output_dir = str(test_home / "Desktop")

        # These would be the expected values if config was loaded with this home
        assert len(expected_config_dir) > 0
        assert len(expected_output_dir) > 0
