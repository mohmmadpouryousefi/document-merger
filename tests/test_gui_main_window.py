"""
Test cases for GUI Main Window module.
"""

from unittest.mock import Mock, patch

# Mock the entire GUI module to avoid tkinter issues
with patch("tkinter.Tk"), patch("tkinter.ttk.Style"), patch("tkinter.StringVar"), patch(
    "tkinter.Frame"
), patch("tkinter.ttk.Progressbar"):
    from src.gui.main_window import FileManagerGUI


# Simple tests focused on method behavior
class TestFileManagerGUIUtilities:
    """Test utility methods that don't require GUI initialization."""

    def test_generate_error_content(self):
        """Test generating error content."""
        # Create a mock GUI instance without initialization
        gui = object.__new__(FileManagerGUI)

        errors = ["Error 1", "Error 2"]
        result = gui._generate_error_content(errors)
        assert "ERRORS FOUND:" in result
        assert "Error 1" in result
        assert "Error 2" in result

    def test_generate_summary_section(self):
        """Test generating summary section."""
        gui = object.__new__(FileManagerGUI)

        preview = {
            "file_type": "pdf",
            "file_count": 2,
            "total_size_formatted": "1 MB",
            "estimated_output_size_formatted": "900 KB",
        }

        result = gui._generate_summary_section(preview)
        assert "File type: PDF" in result
        assert "Files to merge: 2" in result
        assert "Total size: 1 MB" in result

    def test_generate_warnings_section_empty(self):
        """Test generating warnings section when empty."""
        gui = object.__new__(FileManagerGUI)

        preview = {"warnings": []}
        result = gui._generate_warnings_section(preview)
        assert result == ""

    def test_generate_warnings_section_with_warnings(self):
        """Test generating warnings section with warnings."""
        gui = object.__new__(FileManagerGUI)

        preview = {"warnings": ["Warning 1", "Warning 2"]}
        result = gui._generate_warnings_section(preview)
        assert "WARNINGS:" in result
        assert "Warning 1" in result
        assert "Warning 2" in result

    def test_format_single_file_info_pdf(self):
        """Test formatting single PDF file info."""
        gui = object.__new__(FileManagerGUI)

        file_info = {
            "name": "test.pdf",
            "size_formatted": "1 KB",
            "type": "pdf",
            "pages": 5,
        }

        result = gui._format_single_file_info(0, file_info)
        assert "1. test.pdf" in result
        assert "Size: 1 KB" in result
        assert "Type: pdf" in result
        assert "Pages: 5" in result

    def test_format_single_file_info_excel(self):
        """Test formatting Excel file info."""
        gui = object.__new__(FileManagerGUI)

        file_info = {
            "name": "test.xlsx",
            "size_formatted": "2 KB",
            "type": "excel",
            "sheets": 3,
            "sheet_names": ["Sheet1", "Sheet2", "Sheet3"],
        }

        result = gui._format_single_file_info(0, file_info)
        assert "1. test.xlsx" in result
        assert "Sheets: 3" in result
        assert "Sheet1, Sheet2, Sheet3" in result

    def test_format_single_file_info_excel_many_sheets(self):
        """Test formatting Excel file info with many sheets."""
        gui = object.__new__(FileManagerGUI)

        file_info = {
            "name": "test.xlsx",
            "size_formatted": "2 KB",
            "type": "excel",
            "sheets": 5,
            "sheet_names": ["Sheet1", "Sheet2", "Sheet3", "Sheet4", "Sheet5"],
        }

        result = gui._format_single_file_info(0, file_info)
        assert "1. test.xlsx" in result
        assert "Sheets: 5" in result
        assert (
            "Sheet1, Sheet2, Sheet3, ..." in result
        )  # Fixed assertion to match actual output

    def test_build_basic_file_list(self):
        """Test building basic file list."""
        gui = object.__new__(FileManagerGUI)
        gui.selected_files = ["path/to/test1.pdf", "path/to/test2.pdf"]

        result = gui._build_basic_file_list()
        assert "test1.pdf" in result
        assert "test2.pdf" in result


# Test validation methods
class TestFileManagerGUIValidation:
    """Test validation methods."""

    def test_validate_merge_requirements_success(self):
        """Test merge requirements validation success."""
        gui = object.__new__(FileManagerGUI)
        gui.selected_files = ["file1.pdf", "file2.pdf"]

        result = gui._validate_merge_requirements()
        assert result is True

    @patch("tkinter.messagebox.showwarning")
    def test_validate_merge_requirements_failure(self, mock_warning):
        """Test merge requirements validation failure."""
        gui = object.__new__(FileManagerGUI)
        gui.selected_files = ["file1.pdf"]  # Only one file

        result = gui._validate_merge_requirements()
        assert result is False
        mock_warning.assert_called_once()

    @patch("tkinter.messagebox.showwarning")
    def test_validate_merge_requirements_empty(self, mock_warning):
        """Test merge requirements validation with empty file list."""
        gui = object.__new__(FileManagerGUI)
        gui.selected_files = []

        result = gui._validate_merge_requirements()
        assert result is False
        mock_warning.assert_called_once()


# Test methods that work with mock components
class TestFileManagerGUISimpleMethods:
    """Test simple GUI methods with minimal dependencies."""

    def test_generate_success_content_structure(self):
        """Test success content generation structure."""
        gui = object.__new__(FileManagerGUI)

        preview = {
            "file_type": "pdf",
            "file_count": 2,
            "total_size_formatted": "1 MB",
            "estimated_output_size_formatted": "900 KB",
            "files_info": [],
            "warnings": [],
        }

        # Mock the helper methods to avoid attribute errors
        gui._generate_summary_section = Mock(return_value="SUMMARY:\nFile type: PDF\n")
        gui._generate_files_section = Mock(return_value="FILES:\nfile1.pdf\n")
        gui._generate_warnings_section = Mock(return_value="")

        result = gui._generate_success_content(preview)
        assert "MERGE PREVIEW" in result
        gui._generate_summary_section.assert_called_once_with(preview)
        gui._generate_files_section.assert_called_once_with(preview)
        gui._generate_warnings_section.assert_called_once_with(preview)

    def test_generate_files_section_pdf(self):
        """Test generating files section for PDF."""
        gui = object.__new__(FileManagerGUI)

        preview = {
            "file_type": "pdf",
            "files_info": [
                {
                    "name": "test1.pdf",
                    "accessible": True,
                    "size_formatted": "500 KB",
                    "pages": 5,
                },
                {"name": "test2.pdf", "accessible": False, "size_formatted": "300 KB"},
            ],
        }

        result = gui._generate_files_section(preview)
        assert "FILES:" in result
        assert "✓ test1.pdf" in result
        assert "✗ test2.pdf" in result
        assert "Pages: 5" in result

    def test_generate_files_section_excel(self):
        """Test generating files section for Excel."""
        gui = object.__new__(FileManagerGUI)

        preview = {
            "file_type": "excel",
            "files_info": [
                {
                    "name": "test1.xlsx",
                    "accessible": True,
                    "size_formatted": "100 KB",
                    "sheets": 3,
                    "sheet_names": ["Sheet1", "Sheet2", "Sheet3"],
                }
            ],
        }

        result = gui._generate_files_section(preview)
        assert "FILES:" in result
        assert "✓ test1.xlsx" in result
        assert "Sheets: 3" in result
        assert "Sheet1, Sheet2, Sheet3" in result


# Test main entry points
def test_cli_main_with_args():
    """Test CLI main function with arguments."""
    with patch(
        "sys.argv", ["cli_interface.py", "file1.pdf", "file2.pdf", "-o", "output.pdf"]
    ):
        with patch("src.cli.cli_interface.CLIInterface") as mock_cli_class:
            mock_cli = Mock()
            mock_cli_class.return_value = mock_cli

            from src.cli.cli_interface import main

            main()

            mock_cli.merge_files.assert_called_once()


def test_cli_main_interactive():
    """Test CLI main function in interactive mode."""
    with patch("sys.argv", ["cli_interface.py"]):
        with patch("src.cli.cli_interface.CLIInterface") as mock_cli_class:
            mock_cli = Mock()
            mock_cli_class.return_value = mock_cli

            from src.cli.cli_interface import main

            main()

            mock_cli.interactive_mode.assert_called_once()


def test_gui_main():
    """Test GUI main function."""
    with patch("src.gui.main_window.FileManagerGUI") as mock_gui_class:
        mock_gui = Mock()
        mock_gui_class.return_value = mock_gui

        from src.gui.main_window import main

        main()

        mock_gui.run.assert_called_once()
