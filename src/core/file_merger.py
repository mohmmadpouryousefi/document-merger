"""
Main file merger orchestrator that coordinates different file type mergers.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from .excel_merger import ExcelMerger
from .file_detector import FileTypeDetector
from .pdf_merger import PDFMerger


class FileMerger:
    """Main orchestrator for file merging operations."""

    def __init__(self):
        """Initialize the file merger."""
        self.logger = logging.getLogger(__name__)
        self.pdf_merger = PDFMerger()
        self.excel_merger = ExcelMerger()
        self.detector = FileTypeDetector()

        # Setup logging
        self._setup_logging()

    def _setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler("file_merger.log", mode="a"),
            ],
        )

    def merge_files(
        self, input_files: List[str], output_file: str, add_bookmarks: bool = True
    ) -> Dict[str, Any]:
        """
        Merge multiple files of the same type into a single output file.

        Args:
            input_files: List of input file paths
            output_file: Output file path
            add_bookmarks: Whether to add bookmarks (for PDFs)

        Returns:
            Dictionary with operation results
        """
        result = {
            "success": False,
            "message": "",
            "file_type": None,
            "input_count": len(input_files),
            "output_file": output_file,
            "errors": [],
            "warnings": [],
        }

        try:
            # Validate input files
            file_type, valid_files, errors = self.detector.validate_files(input_files)

            if errors:
                result["errors"] = errors
                result["message"] = "; ".join(errors)
                return result

            if not valid_files:
                result["errors"] = ["No valid files found"]
                result["message"] = "No valid files found"
                return result

            result["file_type"] = file_type

            # Additional validation for file accessibility and corruption
            accessible_files = []
            for file_path in valid_files:
                if self.detector.is_file_accessible(file_path):
                    if self._validate_file_integrity(file_path, file_type):
                        accessible_files.append(file_path)
                    else:
                        result["warnings"].append(f"File may be corrupted: {file_path}")
                else:
                    result["errors"].append(f"File not accessible: {file_path}")

            if not accessible_files:
                result["message"] = "No accessible files found"
                return result

            # Generate output filename if not provided or if directory is provided
            output_path = Path(output_file)
            if output_path.is_dir() or not output_path.suffix:
                output_file = self._generate_output_filename(
                    accessible_files, file_type, str(output_path)
                )
                result["output_file"] = output_file

            # Perform the merge based on file type
            if file_type == "pdf":
                success = self._merge_pdf_files(
                    accessible_files, output_file, add_bookmarks
                )
            elif file_type == "excel":
                success = self._merge_excel_files(accessible_files, output_file)
            else:
                result["errors"].append(f"Unsupported file type: {file_type}")
                result["message"] = f"Unsupported file type: {file_type}"
                return result

            if success:
                result["success"] = True
                result[
                    "message"
                ] = f"Successfully merged {len(accessible_files)} {file_type} files"
                self.logger.info(f"Merge completed: {result['message']}")
            else:
                result["message"] = f"Failed to merge {file_type} files"
                result["errors"].append(result["message"])

        except Exception as e:
            error_msg = f"Unexpected error during merge: {str(e)}"
            result["errors"].append(error_msg)
            result["message"] = error_msg
            self.logger.error(error_msg, exc_info=True)

        return result

    def _validate_file_integrity(self, file_path: str, file_type: str) -> bool:
        """
        Validate file integrity based on file type.

        Args:
            file_path: Path to the file
            file_type: Type of file ('pdf' or 'excel')

        Returns:
            True if file is valid, False otherwise
        """
        try:
            if file_type == "pdf":
                return self.pdf_merger.validate_pdf(file_path)
            elif file_type == "excel":
                return self.excel_merger.validate_excel(file_path)
            return True
        except Exception as e:
            self.logger.error(
                f"File integrity validation failed for {file_path}: {str(e)}"
            )
            return False

    def _merge_pdf_files(
        self, files: List[str], output_file: str, add_bookmarks: bool
    ) -> bool:
        """Merge PDF files."""
        if add_bookmarks:
            return self.pdf_merger.merge_with_bookmarks(files, output_file)
        else:
            return self.pdf_merger.merge_pdfs(files, output_file)

    def _merge_excel_files(self, files: List[str], output_file: str) -> bool:
        """Merge Excel files."""
        return self.excel_merger.merge_excel_files(files, output_file)

    def _generate_output_filename(
        self, input_files: List[str], file_type: str, output_dir: str = None
    ) -> str:
        """
        Generate a descriptive output filename.

        Args:
            input_files: List of input file paths
            file_type: Type of files being merged
            output_dir: Output directory (optional)

        Returns:
            Generated output file path
        """
        if not output_dir:
            # Use the directory of the first input file
            output_dir = str(Path(input_files[0]).parent)

        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        extension = ".pdf" if file_type == "pdf" else ".xlsx"
        filename = f"merged_{file_type}_{len(input_files)}files_{timestamp}{extension}"

        return str(Path(output_dir) / filename)

    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """
        Get detailed information about a file.

        Args:
            file_path: Path to the file

        Returns:
            Dictionary with file information
        """
        try:
            file_type = self.detector.detect_file_type(file_path)

            basic_info = {
                "path": file_path,
                "name": Path(file_path).name,
                "size": self.detector.get_file_size(file_path),
                "size_formatted": self.detector.format_file_size(
                    self.detector.get_file_size(file_path)
                ),
                "type": file_type,
                "accessible": self.detector.is_file_accessible(file_path),
            }

            if file_type == "pdf":
                pdf_info = self.pdf_merger.get_pdf_info(file_path)
                basic_info.update(pdf_info)
            elif file_type == "excel":
                excel_info = self.excel_merger.get_excel_info(file_path)
                basic_info.update(excel_info)

            return basic_info

        except Exception as e:
            return {"path": file_path, "error": str(e), "accessible": False}

    def reorder_files(self, files: List[str], new_order: List[int]) -> List[str]:
        """
        Reorder files based on provided indices.

        Args:
            files: Original list of files
            new_order: List of indices representing new order

        Returns:
            Reordered list of files
        """
        try:
            if len(new_order) != len(files):
                raise ValueError("New order must have same length as files list")

            if set(new_order) != set(range(len(files))):
                raise ValueError(
                    "New order must contain all indices from 0 to len(files)-1"
                )

            return [files[i] for i in new_order]

        except Exception as e:
            self.logger.error(f"File reordering failed: {str(e)}")
            return files  # Return original order if reordering fails

    def preview_merge(self, input_files: List[str]) -> Dict[str, Any]:
        """
        Preview what would happen during a merge without actually performing it.

        Args:
            input_files: List of input file paths

        Returns:
            Dictionary with preview information
        """
        preview = {
            "valid": False,
            "file_type": None,
            "file_count": len(input_files),
            "files_info": [],
            "total_size": 0,
            "estimated_output_size": 0,
            "errors": [],
            "warnings": [],
        }

        try:
            # Validate files
            file_type, valid_files, errors = self.detector.validate_files(input_files)

            if errors:
                preview["errors"] = errors
                return preview

            preview["file_type"] = file_type
            preview["valid"] = True

            # Get detailed info for each file
            total_size = 0
            for file_path in valid_files:
                file_info = self.get_file_info(file_path)
                preview["files_info"].append(file_info)
                total_size += file_info.get("size", 0)

            preview["total_size"] = total_size
            preview["total_size_formatted"] = self.detector.format_file_size(total_size)

            # Estimate output size (usually slightly larger due to metadata)
            preview["estimated_output_size"] = int(total_size * 1.1)
            preview["estimated_output_size_formatted"] = self.detector.format_file_size(
                preview["estimated_output_size"]
            )

        except Exception as e:
            preview["errors"].append(f"Preview failed: {str(e)}")

        return preview
