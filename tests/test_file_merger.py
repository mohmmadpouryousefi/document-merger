"""
Unit tests for file merger orchestrator.
"""

import unittest
import tempfile
import os
import shutil
from unittest.mock import patch, MagicMock

# Add src to path for testing
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

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
    
    @patch('core.file_merger.PDFMerger')
    def test_merge_pdf_files(self, mock_pdf_merger_class):
        """Test PDF file merging through orchestrator."""
        mock_pdf_merger = mock_pdf_merger_class.return_value
        mock_pdf_merger.merge_pdfs.return_value = True
        
        pdf_files = ['file1.pdf', 'file2.pdf']
        output_file = 'merged.pdf'
        
        result = self.merger.merge_files(pdf_files, output_file, add_bookmarks=False)
        
        self.assertTrue(result)
        mock_pdf_merger.merge_pdfs.assert_called_once_with(pdf_files, output_file)
    
    @patch('core.file_merger.PDFMerger')
    def test_merge_pdf_files_with_bookmarks(self, mock_pdf_merger_class):
        """Test PDF file merging with bookmarks through orchestrator."""
        mock_pdf_merger = mock_pdf_merger_class.return_value
        mock_pdf_merger.merge_with_bookmarks.return_value = True
        
        pdf_files = ['chapter1.pdf', 'chapter2.pdf']
        output_file = 'book.pdf'
        
        result = self.merger.merge_files(pdf_files, output_file, add_bookmarks=True)
        
        self.assertTrue(result)
        mock_pdf_merger.merge_with_bookmarks.assert_called_once_with(pdf_files, output_file)
    
    @patch('core.file_merger.ExcelMerger')
    def test_merge_excel_files(self, mock_excel_merger_class):
        """Test Excel file merging through orchestrator."""
        mock_excel_merger = mock_excel_merger_class.return_value
        mock_excel_merger.merge_excel_files.return_value = True
        
        excel_files = ['data1.xlsx', 'data2.xlsx']
        output_file = 'combined.xlsx'
        
        result = self.merger.merge_files(excel_files, output_file)
        
        self.assertTrue(result)
        mock_excel_merger.merge_excel_files.assert_called_once_with(excel_files, output_file)
    
    @patch('core.file_merger.FileDetector')
    def test_unsupported_file_type(self, mock_detector_class):
        """Test handling of unsupported file types."""
        mock_detector = mock_detector_class.return_value
        mock_detector.detect_file_types.return_value = ['txt']
        
        text_files = ['file1.txt', 'file2.txt']
        output_file = 'combined.txt'
        
        result = self.merger.merge_files(text_files, output_file)
        
        self.assertFalse(result)
    
    @patch('core.file_merger.FileDetector')
    def test_mixed_file_types(self, mock_detector_class):
        """Test handling of mixed file types."""
        mock_detector = mock_detector_class.return_value
        mock_detector.detect_file_types.return_value = ['pdf', 'xlsx']
        
        mixed_files = ['document.pdf', 'spreadsheet.xlsx']
        output_file = 'combined.pdf'
        
        result = self.merger.merge_files(mixed_files, output_file)
        
        self.assertFalse(result)
    
    @patch('core.file_merger.FileDetector')
    @patch('core.file_merger.PDFMerger')
    def test_validate_files_success(self, mock_pdf_merger_class, mock_detector_class):
        """Test successful file validation."""
        mock_detector = mock_detector_class.return_value
        mock_detector.detect_file_types.return_value = ['pdf']
        
        mock_pdf_merger = mock_pdf_merger_class.return_value
        mock_pdf_merger.validate_pdf.return_value = True
        
        pdf_files = ['valid1.pdf', 'valid2.pdf']
        
        result = self.merger.validate_files(pdf_files)
        
        self.assertTrue(result)
    
    @patch('core.file_merger.FileDetector')
    @patch('core.file_merger.PDFMerger')
    def test_validate_files_invalid_pdf(self, mock_pdf_merger_class, mock_detector_class):
        """Test validation with invalid PDF."""
        mock_detector = mock_detector_class.return_value
        mock_detector.detect_file_types.return_value = ['pdf']
        
        mock_pdf_merger = mock_pdf_merger_class.return_value
        mock_pdf_merger.validate_pdf.side_effect = [True, False]  # Second file invalid
        
        pdf_files = ['valid.pdf', 'invalid.pdf']
        
        result = self.merger.validate_files(pdf_files)
        
        self.assertFalse(result)
    
    @patch('core.file_merger.FileDetector')
    @patch('core.file_merger.ExcelMerger')
    def test_validate_excel_files(self, mock_excel_merger_class, mock_detector_class):
        """Test Excel file validation."""
        mock_detector = mock_detector_class.return_value
        mock_detector.detect_file_types.return_value = ['xlsx']
        
        mock_excel_merger = mock_excel_merger_class.return_value
        mock_excel_merger.validate_excel.return_value = True
        
        excel_files = ['data1.xlsx', 'data2.xlsx']
        
        result = self.merger.validate_files(excel_files)
        
        self.assertTrue(result)
    
    def test_get_file_info_empty_list(self):
        """Test getting file info with empty file list."""
        result = self.merger.get_file_info([])
        
        self.assertEqual(result, {})
    
    @patch('core.file_merger.FileDetector')
    @patch('core.file_merger.PDFMerger')
    def test_get_pdf_file_info(self, mock_pdf_merger_class, mock_detector_class):
        """Test getting PDF file information."""
        mock_detector = mock_detector_class.return_value
        mock_detector.detect_file_types.return_value = ['pdf']
        
        mock_pdf_merger = mock_pdf_merger_class.return_value
        mock_pdf_merger.get_pdf_info.return_value = {'pages': 5, 'title': 'Test Doc'}
        
        pdf_files = ['document.pdf']
        
        result = self.merger.get_file_info(pdf_files)
        
        self.assertIn('document.pdf', result)
        self.assertEqual(result['document.pdf']['pages'], 5)
        self.assertEqual(result['document.pdf']['title'], 'Test Doc')
    
    @patch('core.file_merger.FileDetector')
    @patch('core.file_merger.ExcelMerger')
    def test_get_excel_file_info(self, mock_excel_merger_class, mock_detector_class):
        """Test getting Excel file information."""
        mock_detector = mock_detector_class.return_value
        mock_detector.detect_file_types.return_value = ['xlsx']
        
        mock_excel_merger = mock_excel_merger_class.return_value
        mock_excel_merger.get_excel_info.return_value = {'sheets': 3, 'total_rows': 100}
        
        excel_files = ['spreadsheet.xlsx']
        
        result = self.merger.get_file_info(excel_files)
        
        self.assertIn('spreadsheet.xlsx', result)
        self.assertEqual(result['spreadsheet.xlsx']['sheets'], 3)
        self.assertEqual(result['spreadsheet.xlsx']['total_rows'], 100)


class TestFileMergerErrorHandling(unittest.TestCase):
    """Test error handling in FileMerger."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.merger = FileMerger()
    
    def test_merge_files_empty_list(self):
        """Test merging with empty file list."""
        result = self.merger.merge_files([], 'output.pdf')
        
        self.assertFalse(result)
    
    def test_merge_files_none_input(self):
        """Test merging with None input."""
        result = self.merger.merge_files(None, 'output.pdf')
        
        self.assertFalse(result)
    
    def test_merge_files_empty_output(self):
        """Test merging with empty output filename."""
        result = self.merger.merge_files(['file1.pdf'], '')
        
        self.assertFalse(result)
    
    @patch('core.file_merger.FileDetector')
    def test_merge_files_detector_error(self, mock_detector_class):
        """Test handling of file detector errors."""
        mock_detector = mock_detector_class.return_value
        mock_detector.detect_file_types.side_effect = Exception("Detector error")
        
        result = self.merger.merge_files(['file1.pdf'], 'output.pdf')
        
        self.assertFalse(result)
    
    @patch('core.file_merger.FileDetector')
    @patch('core.file_merger.PDFMerger')
    def test_merge_files_merger_error(self, mock_pdf_merger_class, mock_detector_class):
        """Test handling of merger errors."""
        mock_detector = mock_detector_class.return_value
        mock_detector.detect_file_types.return_value = ['pdf']
        
        mock_pdf_merger = mock_pdf_merger_class.return_value
        mock_pdf_merger.merge_pdfs.side_effect = Exception("Merge error")
        
        result = self.merger.merge_files(['file1.pdf'], 'output.pdf')
        
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
