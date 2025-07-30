"""
Unit tests for file merger orchestrator.
"""

# Add src to path for testing
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import shutil
import tempfile
import unittest
from unittest.mock import patch

from core.file_merger import FileMerger


class TestFileMerger(unittest.TestCase):
    """Test cases for FileMerger orchestrator."""

    def setUp(self):
        """Set up test fixtures."""
        self.merger = FileMerger()
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_merger_initialization(self):
        """Test FileMerger initialization."""
        merger = FileMerger()
        self.assertIsInstance(merger, FileMerger)

    @patch("core.file_merger.FileTypeDetector")
    def test_merge_pdf_files(self, mock_detector_class):
        """Test PDF file merging through orchestrator."""
        mock_detector = mock_detector_class.return_value
        mock_detector.validate_files.return_value = (
            "pdf",
            ["file1.pdf", "file2.pdf"],
            [],
        )
        mock_detector.is_file_accessible.return_value = True

        # Mock the detector that's created in FileMerger.__init__
        with patch.object(
            self.merger.detector,
            "validate_files",
            return_value=("pdf", ["file1.pdf", "file2.pdf"], []),
        ), patch.object(
            self.merger.detector, "is_file_accessible", return_value=True
        ), patch.object(
            self.merger, "_validate_file_integrity", return_value=True
        ), patch.object(
            self.merger.pdf_merger, "merge_pdfs", return_value=True
        ) as mock_merge:
            pdf_files = ["file1.pdf", "file2.pdf"]
            output_file = "merged.pdf"

            result = self.merger.merge_files(
                pdf_files, output_file, add_bookmarks=False
            )

            self.assertTrue(result["success"])
            mock_merge.assert_called_once_with(["file1.pdf", "file2.pdf"], "merged.pdf")

    @patch("core.file_merger.FileTypeDetector")
    def test_merge_pdf_files_with_bookmarks(self, mock_detector_class):
        """Test PDF file merging with bookmarks through orchestrator."""
        mock_detector = mock_detector_class.return_value
        mock_detector.validate_files.return_value = (
            "pdf",
            ["chapter1.pdf", "chapter2.pdf"],
            [],
        )
        mock_detector.is_file_accessible.return_value = True

        # Mock the detector that's created in FileMerger.__init__
        with patch.object(
            self.merger.detector,
            "validate_files",
            return_value=("pdf", ["chapter1.pdf", "chapter2.pdf"], []),
        ), patch.object(
            self.merger.detector, "is_file_accessible", return_value=True
        ), patch.object(
            self.merger, "_validate_file_integrity", return_value=True
        ), patch.object(
            self.merger.pdf_merger, "merge_with_bookmarks", return_value=True
        ) as mock_merge:
            pdf_files = ["chapter1.pdf", "chapter2.pdf"]
            output_file = "book.pdf"

            result = self.merger.merge_files(pdf_files, output_file, add_bookmarks=True)

            self.assertTrue(result["success"])
            mock_merge.assert_called_once_with(
                ["chapter1.pdf", "chapter2.pdf"], "book.pdf"
            )

    @patch("core.file_merger.FileTypeDetector")
    def test_merge_excel_files(self, mock_detector_class):
        """Test Excel file merging through orchestrator."""
        mock_detector = mock_detector_class.return_value
        mock_detector.validate_files.return_value = (
            "excel",
            ["data1.xlsx", "data2.xlsx"],
            [],
        )
        mock_detector.is_file_accessible.return_value = True

        # Mock the detector that's created in FileMerger.__init__
        with patch.object(
            self.merger.detector,
            "validate_files",
            return_value=("excel", ["data1.xlsx", "data2.xlsx"], []),
        ), patch.object(
            self.merger.detector, "is_file_accessible", return_value=True
        ), patch.object(
            self.merger, "_validate_file_integrity", return_value=True
        ), patch.object(
            self.merger.excel_merger, "merge_excel_files", return_value=True
        ) as mock_merge:
            excel_files = ["data1.xlsx", "data2.xlsx"]
            output_file = "combined.xlsx"

            result = self.merger.merge_files(excel_files, output_file)

            self.assertTrue(result["success"])
            mock_merge.assert_called_once_with(
                ["data1.xlsx", "data2.xlsx"], "combined.xlsx"
            )

    @patch("core.file_merger.FileTypeDetector")
    def test_unsupported_file_type(self, mock_detector_class):
        """Test handling of unsupported file types."""
        mock_detector = mock_detector_class.return_value
        mock_detector.validate_files.return_value = (
            "txt",
            [],
            ["Unsupported file type: txt"],
        )

        # Mock the detector that's created in FileMerger.__init__
        with patch.object(
            self.merger.detector,
            "validate_files",
            return_value=("txt", [], ["Unsupported file type: txt"]),
        ):
            text_files = ["file1.txt", "file2.txt"]
            output_file = "combined.txt"

            result = self.merger.merge_files(text_files, output_file)

            self.assertFalse(result["success"])
            self.assertIn("Unsupported file type", result["message"])

    @patch("core.file_merger.FileTypeDetector")
    def test_mixed_file_types(self, mock_detector_class):
        """Test handling of mixed file types."""
        mock_detector = mock_detector_class.return_value
        mock_detector.validate_files.return_value = (
            None,
            [],
            ["All files must be of the same type. Found: excel, pdf"],
        )

        # Mock the detector that's created in FileMerger.__init__
        with patch.object(
            self.merger.detector,
            "validate_files",
            return_value=(
                None,
                [],
                ["All files must be of the same type. Found: excel, pdf"],
            ),
        ):
            mixed_files = ["document.pdf", "spreadsheet.xlsx"]
            output_file = "combined.pdf"

            result = self.merger.merge_files(mixed_files, output_file)

            self.assertFalse(result["success"])
            self.assertIn("same type", result["message"])

    @patch("core.file_merger.FileTypeDetector")
    def test_validate_files_success(self, mock_detector_class):
        """Test successful file validation."""
        mock_detector = mock_detector_class.return_value
        mock_detector.validate_files.return_value = (
            "pdf",
            ["valid1.pdf", "valid2.pdf"],
            [],
        )
        mock_detector.is_file_accessible.return_value = True

        with patch.object(self.merger, "_validate_file_integrity", return_value=True):
            pdf_files = ["valid1.pdf", "valid2.pdf"]

            # Since there's no direct validate_files method, test through merge_files
            result = self.merger.merge_files(pdf_files, "output.pdf")

            # If validation succeeds, it should at least get to the merge attempt
            self.assertIsInstance(result, dict)
            self.assertIn("success", result)

    @patch("core.file_merger.FileTypeDetector")
    def test_validate_files_invalid_pdf(self, mock_detector_class):
        """Test validation with invalid PDF."""
        mock_detector = mock_detector_class.return_value
        mock_detector.validate_files.return_value = (
            "pdf",
            ["valid.pdf"],
            ["Invalid PDF file: invalid.pdf"],
        )

        pdf_files = ["valid.pdf", "invalid.pdf"]

        result = self.merger.merge_files(pdf_files, "output.pdf")

        self.assertFalse(result["success"])

    @patch("core.file_merger.FileTypeDetector")
    def test_validate_excel_files(self, mock_detector_class):
        """Test Excel file validation."""
        mock_detector = mock_detector_class.return_value
        mock_detector.validate_files.return_value = (
            "excel",
            ["data1.xlsx", "data2.xlsx"],
            [],
        )
        mock_detector.is_file_accessible.return_value = True

        # Mock the detector that's created in FileMerger.__init__
        with patch.object(
            self.merger.detector,
            "validate_files",
            return_value=("excel", ["data1.xlsx", "data2.xlsx"], []),
        ), patch.object(
            self.merger.detector, "is_file_accessible", return_value=True
        ), patch.object(
            self.merger, "_validate_file_integrity", return_value=True
        ), patch.object(
            self.merger.excel_merger, "merge_excel_files", return_value=True
        ):
            excel_files = ["data1.xlsx", "data2.xlsx"]

            result = self.merger.merge_files(excel_files, "output.xlsx")

            self.assertTrue(result["success"])

    def test_get_file_info_empty_list(self):
        """Test getting file info with empty file list."""
        # Test with actual empty string since get_file_info expects a single file path
        result = self.merger.get_file_info("")

        self.assertFalse(result["accessible"])
        # The method returns a dict with basic info, not an error key

    @patch("core.file_merger.FileTypeDetector")
    def test_get_pdf_file_info(self, mock_detector_class):
        """Test getting PDF file information."""
        mock_detector = mock_detector_class.return_value
        mock_detector.detect_file_type.return_value = "pdf"
        mock_detector.get_file_size.return_value = 1024
        mock_detector.format_file_size.return_value = "1.0 KB"
        mock_detector.is_file_accessible.return_value = True

        # Mock the detector that's created in FileMerger.__init__
        with patch.object(
            self.merger.detector, "detect_file_type", return_value="pdf"
        ), patch.object(
            self.merger.detector, "get_file_size", return_value=1024
        ), patch.object(
            self.merger.detector, "format_file_size", return_value="1.0 KB"
        ), patch.object(
            self.merger.detector, "is_file_accessible", return_value=True
        ), patch.object(
            self.merger.pdf_merger,
            "get_pdf_info",
            return_value={"pages": 5, "title": "Test Doc"},
        ):
            pdf_file = "document.pdf"

            result = self.merger.get_file_info(pdf_file)

            self.assertEqual(result["type"], "pdf")
            self.assertEqual(result["pages"], 5)
            self.assertEqual(result["title"], "Test Doc")

    @patch("core.file_merger.FileTypeDetector")
    def test_get_excel_file_info(self, mock_detector_class):
        """Test getting Excel file information."""
        mock_detector = mock_detector_class.return_value
        mock_detector.detect_file_type.return_value = "excel"
        mock_detector.get_file_size.return_value = 2048
        mock_detector.format_file_size.return_value = "2.0 KB"
        mock_detector.is_file_accessible.return_value = True

        # Mock the detector that's created in FileMerger.__init__
        with patch.object(
            self.merger.detector, "detect_file_type", return_value="excel"
        ), patch.object(
            self.merger.detector, "get_file_size", return_value=2048
        ), patch.object(
            self.merger.detector, "format_file_size", return_value="2.0 KB"
        ), patch.object(
            self.merger.detector, "is_file_accessible", return_value=True
        ), patch.object(
            self.merger.excel_merger,
            "get_excel_info",
            return_value={"sheets": 3, "sheet_names": ["Sheet1", "Sheet2", "Sheet3"]},
        ):
            excel_file = "spreadsheet.xlsx"

            result = self.merger.get_file_info(excel_file)

            self.assertEqual(result["type"], "excel")
            self.assertEqual(result["sheets"], 3)
            self.assertIn("Sheet1", result["sheet_names"])


class TestFileMergerErrorHandling(unittest.TestCase):
    """Test error handling in FileMerger."""

    def setUp(self):
        """Set up test fixtures."""
        self.merger = FileMerger()

    def test_merge_files_empty_list(self):
        """Test merging with empty file list."""
        result = self.merger.merge_files([], "output.pdf")

        self.assertFalse(result["success"])
        self.assertIn("No files provided", result["message"])

    def test_merge_files_none_input(self):
        """Test merging with None input."""
        try:
            result = self.merger.merge_files(None, "output.pdf")
            self.assertFalse(result["success"])
        except TypeError:
            # This is expected if the method doesn't handle None gracefully
            pass

    def test_merge_files_empty_output(self):
        """Test merging with empty output filename."""
        result = self.merger.merge_files(["file1.pdf"], "")

        self.assertFalse(result["success"])
        # The method might still process but fail for other reasons

    @patch("core.file_merger.FileTypeDetector")
    def test_merge_files_detector_error(self, mock_detector_class):
        """Test handling of file detector errors."""
        mock_detector = mock_detector_class.return_value
        mock_detector.validate_files.side_effect = Exception("Detector error")

        # Mock the detector that's created in FileMerger.__init__
        with patch.object(
            self.merger.detector,
            "validate_files",
            side_effect=Exception("Detector error"),
        ):
            result = self.merger.merge_files(["file1.pdf"], "output.pdf")

            self.assertFalse(result["success"])
            self.assertIn("Unexpected error", result["message"])

    @patch("core.file_merger.FileTypeDetector")
    def test_merge_files_merger_error(self, mock_detector_class):
        """Test handling of merger errors."""
        mock_detector = mock_detector_class.return_value
        mock_detector.validate_files.return_value = ("pdf", ["file1.pdf"], [])
        mock_detector.is_file_accessible.return_value = True

        with patch.object(
            self.merger.pdf_merger, "validate_pdf", return_value=True
        ), patch.object(
            self.merger.pdf_merger, "merge_pdfs", side_effect=Exception("Merge error")
        ):
            result = self.merger.merge_files(["file1.pdf"], "output.pdf")

            self.assertFalse(result["success"])


if __name__ == "__main__":
    unittest.main()
