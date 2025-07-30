"""
Unit tests for PDF merger functionality.
"""

import os
import shutil

# Add src to path for testing
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import mock_open, patch

import PyPDF2

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from core.pdf_merger import PDFMerger


class TestPDFMerger(unittest.TestCase):
    """Test cases for PDFMerger class."""

    def setUp(self):
        """Set up test fixtures."""
        self.merger = PDFMerger()
        self.test_dir = tempfile.mkdtemp()

        # Create test PDF content
        self.test_pdf_content = b"""%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj

2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj

3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
>>
endobj

xref
0 4
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
trailer
<<
/Size 4
/Root 1 0 R
>>
startxref
175
%%EOF"""

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def create_test_pdf(self, filename, content=None):
        """Create a test PDF file."""
        if content is None:
            content = self.test_pdf_content

        filepath = os.path.join(self.test_dir, filename)
        with open(filepath, "wb") as f:
            f.write(content)
        return filepath

    def test_merger_initialization(self):
        """Test PDFMerger initialization."""
        merger = PDFMerger()
        self.assertIsInstance(merger, PDFMerger)
        self.assertIsNotNone(merger.logger)

    def test_validate_pdf_valid_file(self):
        """Test PDF validation with valid file."""
        pdf_file = self.create_test_pdf("valid.pdf")

        # Mock PyPDF2.PdfReader to avoid actual PDF parsing
        with patch("core.pdf_merger.PyPDF2.PdfReader") as mock_reader:
            mock_reader.return_value.pages = [None]  # At least one page

            result = self.merger.validate_pdf(pdf_file)
            self.assertTrue(result)

    def test_validate_pdf_invalid_file(self):
        """Test PDF validation with invalid file."""
        invalid_file = self.create_test_pdf("invalid.pdf", b"invalid content")

        result = self.merger.validate_pdf(invalid_file)
        self.assertFalse(result)

    def test_validate_pdf_nonexistent_file(self):
        """Test PDF validation with non-existent file."""
        nonexistent_file = os.path.join(self.test_dir, "nonexistent.pdf")

        result = self.merger.validate_pdf(nonexistent_file)
        self.assertFalse(result)

    def test_get_pdf_info_success(self):
        """Test getting PDF info from valid file."""
        pdf_file = self.create_test_pdf("info_test.pdf")

        with patch("core.pdf_merger.PyPDF2.PdfReader") as mock_reader:
            # Mock PDF reader with metadata
            mock_instance = mock_reader.return_value
            mock_instance.pages = [None, None]  # 2 pages
            mock_instance.metadata.title = "Test Document"
            mock_instance.metadata.author = "Test Author"
            mock_instance.metadata.subject = "Test Subject"
            mock_instance.metadata.creator = "Test Creator"
            mock_instance.is_encrypted = False

            info = self.merger.get_pdf_info(pdf_file)

            self.assertEqual(info["pages"], 2)
            self.assertEqual(info["title"], "Test Document")
            self.assertEqual(info["author"], "Test Author")
            self.assertEqual(info["subject"], "Test Subject")
            self.assertEqual(info["creator"], "Test Creator")
            self.assertFalse(info["encrypted"])

    def test_get_pdf_info_no_metadata(self):
        """Test getting PDF info from file without metadata."""
        pdf_file = self.create_test_pdf("no_metadata.pdf")

        with patch("core.pdf_merger.PyPDF2.PdfReader") as mock_reader:
            mock_instance = mock_reader.return_value
            mock_instance.pages = [None]
            mock_instance.metadata = None
            mock_instance.is_encrypted = False

            info = self.merger.get_pdf_info(pdf_file)

            self.assertEqual(info["pages"], 1)
            self.assertIsNone(info["title"])
            self.assertIsNone(info["author"])
            self.assertIsNone(info["subject"])
            self.assertIsNone(info["creator"])
            self.assertFalse(info["encrypted"])

    def test_get_pdf_info_error(self):
        """Test getting PDF info from corrupted file."""
        invalid_file = self.create_test_pdf("corrupted.pdf", b"corrupted")

        info = self.merger.get_pdf_info(invalid_file)

        self.assertEqual(info["pages"], 0)
        self.assertIn("error", info)

    @patch("core.pdf_merger.PyPDF2.PdfMerger")
    def test_merge_pdfs_success(self, mock_merger_class):
        """Test successful PDF merging."""
        # Create test files
        pdf1 = self.create_test_pdf("file1.pdf")
        pdf2 = self.create_test_pdf("file2.pdf")
        output_file = os.path.join(self.test_dir, "merged.pdf")

        # Mock the PdfMerger
        mock_merger = mock_merger_class.return_value

        result = self.merger.merge_pdfs([pdf1, pdf2], output_file)

        self.assertTrue(result)
        mock_merger.append.assert_any_call(pdf1)
        mock_merger.append.assert_any_call(pdf2)
        mock_merger.write.assert_called_once()
        mock_merger.close.assert_called_once()

    @patch("core.pdf_merger.PyPDF2.PdfMerger")
    def test_merge_pdfs_append_error(self, mock_merger_class):
        """Test PDF merging with append error."""
        pdf1 = self.create_test_pdf("file1.pdf")
        pdf2 = self.create_test_pdf("file2.pdf")
        output_file = os.path.join(self.test_dir, "merged.pdf")

        # Mock the PdfMerger to raise exception on append
        mock_merger = mock_merger_class.return_value
        mock_merger.append.side_effect = Exception("Append failed")

        result = self.merger.merge_pdfs([pdf1, pdf2], output_file)

        self.assertFalse(result)

    @patch("core.pdf_merger.PyPDF2.PdfMerger")
    def test_merge_with_bookmarks_success(self, mock_merger_class):
        """Test successful PDF merging with bookmarks."""
        pdf1 = self.create_test_pdf("chapter1.pdf")
        pdf2 = self.create_test_pdf("chapter2.pdf")
        output_file = os.path.join(self.test_dir, "book.pdf")

        mock_merger = mock_merger_class.return_value

        result = self.merger.merge_with_bookmarks([pdf1, pdf2], output_file)

        self.assertTrue(result)

        # Verify bookmarks were created
        expected_calls = [
            unittest.mock.call(pdf1, outline_item="File 1: chapter1"),
            unittest.mock.call(pdf2, outline_item="File 2: chapter2"),
        ]
        mock_merger.append.assert_has_calls(expected_calls)
        mock_merger.write.assert_called_once()
        mock_merger.close.assert_called_once()

    @patch("core.pdf_merger.PyPDF2.PdfMerger")
    def test_merge_with_bookmarks_error(self, mock_merger_class):
        """Test PDF merging with bookmarks when append fails."""
        pdf1 = self.create_test_pdf("chapter1.pdf")
        output_file = os.path.join(self.test_dir, "book.pdf")

        mock_merger = mock_merger_class.return_value
        mock_merger.append.side_effect = Exception("Bookmark append failed")

        result = self.merger.merge_with_bookmarks([pdf1], output_file)

        self.assertFalse(result)

    def test_output_directory_creation(self):
        """Test that output directories are created automatically."""
        pdf1 = self.create_test_pdf("file1.pdf")
        nested_output = os.path.join(self.test_dir, "subdir", "nested", "output.pdf")

        with patch("core.pdf_merger.PyPDF2.PdfMerger") as mock_merger_class:
            mock_merger = mock_merger_class.return_value

            result = self.merger.merge_pdfs([pdf1], nested_output)

            self.assertTrue(result)
            # Verify directory was created
            self.assertTrue(os.path.exists(os.path.dirname(nested_output)))


class TestPDFMergerIntegration(unittest.TestCase):
    """Integration tests for PDFMerger using real PyPDF2."""

    def setUp(self):
        """Set up integration test fixtures."""
        self.merger = PDFMerger()
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up integration test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def create_simple_pdf(self, filename, title="Test Document"):
        """Create a simple valid PDF for integration testing."""
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas

        filepath = os.path.join(self.test_dir, filename)

        try:
            c = canvas.Canvas(filepath, pagesize=letter)
            c.setTitle(title)
            c.drawString(100, 750, f"This is {filename}")
            c.drawString(100, 730, "Test content for integration testing")
            c.showPage()
            c.save()
            return filepath
        except ImportError:
            # If reportlab is not available, skip integration tests
            self.skipTest("reportlab not available for integration testing")

    def test_real_pdf_merge_integration(self):
        """Integration test with real PDF files."""
        try:
            pdf1 = self.create_simple_pdf("real1.pdf", "Document 1")
            pdf2 = self.create_simple_pdf("real2.pdf", "Document 2")
            output_file = os.path.join(self.test_dir, "integrated.pdf")

            result = self.merger.merge_pdfs([pdf1, pdf2], output_file)

            self.assertTrue(result)
            self.assertTrue(os.path.exists(output_file))

            # Verify merged PDF has content from both files
            with open(output_file, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                self.assertGreaterEqual(len(reader.pages), 2)

        except ImportError:
            self.skipTest("reportlab not available for real PDF testing")


if __name__ == "__main__":
    unittest.main()
