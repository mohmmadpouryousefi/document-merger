"""
File type detection and validation utilities.
"""

import mimetypes
import os
from pathlib import Path
from typing import List, Optional, Tuple


class FileTypeDetector:
    """Detects and validates file types for merging operations."""

    SUPPORTED_TYPES = {"pdf": [".pdf"], "excel": [".xlsx", ".xls", ".xlsm"]}

    MIME_TYPE_MAPPING = {
        "application/pdf": "pdf",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "excel",
        "application/vnd.ms-excel": "excel",
        "application/vnd.ms-excel.sheet.macroEnabled.12": "excel",
    }

    @classmethod
    def detect_file_type(cls, file_path: str) -> Optional[str]:
        """
        Detect the file type based on extension and MIME type.

        Args:
            file_path: Path to the file

        Returns:
            File type ('pdf' or 'excel') or None if unsupported
        """
        path = Path(file_path)

        # Check if file exists
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Check file extension
        extension = path.suffix.lower()
        for file_type, extensions in cls.SUPPORTED_TYPES.items():
            if extension in extensions:
                return file_type

        # Fallback to MIME type detection
        mime_type, _ = mimetypes.guess_type(str(path))
        if mime_type in cls.MIME_TYPE_MAPPING:
            return cls.MIME_TYPE_MAPPING[mime_type]

        return None

    @classmethod
    def validate_files(cls, file_paths: List[str]) -> Tuple[str, List[str], List[str]]:
        """
        Validate a list of files for merging.

        Args:
            file_paths: List of file paths to validate

        Returns:
            Tuple of (file_type, valid_files, error_messages)
        """
        if not file_paths:
            return None, [], ["No files provided"]

        if len(file_paths) < 2:
            return None, [], ["At least 2 files are required for merging"]

        valid_files = []
        error_messages = []
        detected_types = set()

        for file_path in file_paths:
            try:
                file_type = cls.detect_file_type(file_path)
                if file_type:
                    detected_types.add(file_type)
                    valid_files.append(file_path)
                else:
                    error_messages.append(f"Unsupported file type: {file_path}")
            except FileNotFoundError as e:
                error_messages.append(str(e))
            except Exception as e:
                error_messages.append(f"Error processing {file_path}: {str(e)}")

        # Check if all files are of the same type
        if len(detected_types) > 1:
            error_messages.append(
                f"All files must be of the same type. Found: {', '.join(detected_types)}"
            )
            return None, [], error_messages
        elif len(detected_types) == 1:
            return detected_types.pop(), valid_files, error_messages
        else:
            return None, [], error_messages

    @classmethod
    def is_file_accessible(cls, file_path: str) -> bool:
        """
        Check if a file is accessible for reading.

        Args:
            file_path: Path to the file

        Returns:
            True if file is accessible, False otherwise
        """
        try:
            path = Path(file_path)
            return path.exists() and path.is_file() and os.access(path, os.R_OK)
        except Exception:
            return False

    @classmethod
    def get_file_size(cls, file_path: str) -> int:
        """
        Get file size in bytes.

        Args:
            file_path: Path to the file

        Returns:
            File size in bytes
        """
        try:
            return Path(file_path).stat().st_size
        except Exception:
            return 0

    @classmethod
    def format_file_size(cls, size_bytes: int) -> str:
        """
        Format file size in human-readable format.

        Args:
            size_bytes: Size in bytes

        Returns:
            Formatted size string
        """
        if size_bytes == 0:
            return "0 B"

        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1

        return f"{size_bytes:.1f} {size_names[i]}"
