"""
Test cases for CLI Interface module.
"""

import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from src.cli.cli_interface import CLIInterface


class TestCLIInterface:
    """Test cases for CLIInterface class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.cli = CLIInterface()
        self.temp_dir = tempfile.mkdtemp()

        # Create test files
        self.test_pdf1 = Path(self.temp_dir) / "test1.pdf"
        self.test_pdf2 = Path(self.temp_dir) / "test2.pdf"
        self.test_excel1 = Path(self.temp_dir) / "test1.xlsx"
        self.test_excel2 = Path(self.temp_dir) / "test2.xlsx"

        # Create dummy files
        for file_path in [
            self.test_pdf1,
            self.test_pdf2,
            self.test_excel1,
            self.test_excel2,
        ]:
            file_path.write_text("dummy content")

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_cli_initialization(self):
        """Test CLI interface initialization."""
        cli = CLIInterface()
        assert cli.merger is not None
        assert cli.detector is not None

    @patch.object(CLIInterface, "_get_input_files")
    @patch.object(CLIInterface, "_show_preview")
    @patch.object(CLIInterface, "_confirm_merge")
    @patch.object(CLIInterface, "_handle_reordering")
    @patch.object(CLIInterface, "_get_output_file")
    @patch.object(CLIInterface, "_get_merge_options")
    @patch.object(CLIInterface, "_perform_merge")
    @patch("builtins.print")
    def test_interactive_mode_success(
        self,
        mock_print,
        mock_perform,
        mock_options,
        mock_output,
        mock_reorder,
        mock_confirm,
        mock_preview,
        mock_input_files,
    ):
        """Test successful interactive mode execution."""
        # Setup mocks
        test_files = [str(self.test_pdf1), str(self.test_pdf2)]
        mock_input_files.return_value = test_files
        mock_confirm.return_value = True
        mock_reorder.return_value = test_files
        mock_output.return_value = "output.pdf"
        mock_options.return_value = {"add_bookmarks": True}

        # Run interactive mode
        self.cli.interactive_mode()

        # Verify all steps were called
        mock_input_files.assert_called_once()
        mock_preview.assert_called_once_with(test_files)
        mock_confirm.assert_called_once()
        mock_reorder.assert_called_once_with(test_files)
        mock_output.assert_called_once_with(test_files)
        mock_options.assert_called_once()
        mock_perform.assert_called_once()

    @patch.object(CLIInterface, "_get_input_files")
    @patch("builtins.print")
    def test_interactive_mode_no_files(self, mock_print, mock_input_files):
        """Test interactive mode with no files selected."""
        mock_input_files.return_value = []

        self.cli.interactive_mode()

        mock_input_files.assert_called_once()
        mock_print.assert_any_call("No files selected. Exiting.")

    @patch.object(CLIInterface, "_get_input_files")
    @patch.object(CLIInterface, "_show_preview")
    @patch.object(CLIInterface, "_confirm_merge")
    @patch("builtins.print")
    def test_interactive_mode_cancelled(
        self, mock_print, mock_confirm, mock_preview, mock_input_files
    ):
        """Test interactive mode when user cancels."""
        test_files = [str(self.test_pdf1), str(self.test_pdf2)]
        mock_input_files.return_value = test_files
        mock_confirm.return_value = False

        self.cli.interactive_mode()

        mock_confirm.assert_called_once()
        mock_print.assert_any_call("Merge cancelled.")

    @patch.object(CLIInterface, "_get_input_files")
    @patch("builtins.print")
    def test_interactive_mode_keyboard_interrupt(self, mock_print, mock_input_files):
        """Test interactive mode with keyboard interrupt."""
        mock_input_files.side_effect = KeyboardInterrupt()

        self.cli.interactive_mode()

        mock_print.assert_any_call("\nOperation cancelled by user.")

    @patch.object(CLIInterface, "_get_input_files")
    @patch("builtins.print")
    def test_interactive_mode_exception(self, mock_print, mock_input_files):
        """Test interactive mode with general exception."""
        mock_input_files.side_effect = Exception("Test error")

        self.cli.interactive_mode()

        mock_print.assert_any_call("\nError: Test error")

    @patch("builtins.input")
    @patch("builtins.print")
    def test_get_input_files_done(self, mock_print, mock_input):
        """Test getting input files with 'done' command."""
        mock_input.side_effect = [str(self.test_pdf1), str(self.test_pdf2), "done"]

        with patch.object(self.cli, "_print_file_input_instructions"):
            result = self.cli._get_input_files()

        assert len(result) == 2
        assert str(self.test_pdf1.resolve()) in result
        assert str(self.test_pdf2.resolve()) in result

    @patch("builtins.input")
    @patch("builtins.print")
    def test_get_input_files_keyboard_interrupt(self, mock_print, mock_input):
        """Test getting input files with keyboard interrupt."""
        mock_input.side_effect = KeyboardInterrupt()

        with patch.object(self.cli, "_print_file_input_instructions"):
            with pytest.raises(KeyboardInterrupt):
                self.cli._get_input_files()

    @patch("builtins.input")
    @patch("builtins.print")
    def test_get_input_files_exception_handling(self, mock_print, mock_input):
        """Test getting input files with exception handling."""
        mock_input.side_effect = [Exception("Test error"), "done"]

        with patch.object(self.cli, "_print_file_input_instructions"):
            with patch.object(
                self.cli,
                "_handle_user_input",
                side_effect=[Exception("Test error"), []],
            ):
                result = self.cli._get_input_files()
                assert result == []

    @patch("builtins.input")
    @patch("builtins.print")
    def test_confirm_merge_yes(self, mock_print, mock_input):
        """Test merge confirmation with yes response."""
        mock_input.return_value = "y"
        result = self.cli._confirm_merge()
        assert result is True

    @patch("builtins.input")
    @patch("builtins.print")
    def test_confirm_merge_no(self, mock_print, mock_input):
        """Test merge confirmation with no response."""
        mock_input.return_value = "n"
        result = self.cli._confirm_merge()
        assert result is False

    @patch("builtins.input")
    @patch("builtins.print")
    def test_confirm_merge_invalid_then_yes(self, mock_print, mock_input):
        """Test merge confirmation with invalid then yes response."""
        mock_input.side_effect = ["invalid", "yes"]
        result = self.cli._confirm_merge()
        assert result is True

    @patch("builtins.input")
    @patch("builtins.print")
    def test_ask_for_reorder_no(self, mock_print, mock_input):
        """Test reorder prompt with no response."""
        mock_input.return_value = "n"
        files = [str(self.test_pdf1), str(self.test_pdf2)]
        result = self.cli._ask_for_reorder(files)
        assert result is False

    @patch("builtins.input")
    @patch("builtins.print")
    def test_ask_for_reorder_yes(self, mock_print, mock_input):
        """Test reorder prompt with yes response."""
        mock_input.return_value = "y"
        files = [str(self.test_pdf1), str(self.test_pdf2)]
        result = self.cli._ask_for_reorder(files)
        assert result is True

    @patch("builtins.print")
    def test_display_current_order(self, mock_print):
        """Test display current order functionality."""
        files = [str(self.test_pdf1), str(self.test_pdf2)]
        self.cli._display_current_order(files)
        # Verify print was called (exact calls depend on implementation)
        assert mock_print.called

    @patch("builtins.print")
    def test_print_file_input_instructions(self, mock_print):
        """Test printing file input instructions."""
        self.cli._print_file_input_instructions()
        assert mock_print.called

    def test_validate_order_correct(self):
        """Test order validation with correct input."""
        files = [str(self.test_pdf1), str(self.test_pdf2)]
        new_order = [1, 0]  # 0-based indexing
        result = self.cli._validate_order(new_order, files)
        assert result is True

    @patch("builtins.print")
    def test_validate_order_wrong_length(self, mock_print):
        """Test order validation with wrong length."""
        files = [str(self.test_pdf1), str(self.test_pdf2)]
        new_order = [0]  # Missing one index
        result = self.cli._validate_order(new_order, files)
        assert result is False

    @patch("builtins.print")
    def test_validate_order_invalid_indices(self, mock_print):
        """Test order validation with invalid indices."""
        files = [str(self.test_pdf1), str(self.test_pdf2)]
        new_order = [0, 2]  # Index 2 doesn't exist
        result = self.cli._validate_order(new_order, files)
        assert result is False

    @patch("builtins.input")
    @patch("builtins.print")
    def test_confirm_new_order_yes(self, mock_print, mock_input):
        """Test confirming new order with yes."""
        mock_input.return_value = "y"
        files = [str(self.test_pdf1), str(self.test_pdf2)]
        result = self.cli._confirm_new_order(files)
        assert result is True

    @patch("builtins.input")
    @patch("builtins.print")
    def test_confirm_new_order_no(self, mock_print, mock_input):
        """Test confirming new order with no."""
        mock_input.return_value = "n"
        files = [str(self.test_pdf1), str(self.test_pdf2)]
        result = self.cli._confirm_new_order(files)
        assert result is False

    def test_handle_single_file_input_existing(self):
        """Test handling single file input with existing file."""
        files = []
        result = self.cli._handle_single_file_input(str(self.test_pdf1), files)
        assert len(result) == 1
        assert str(self.test_pdf1.resolve()) in result

    @patch("builtins.print")
    def test_handle_single_file_input_nonexistent(self, mock_print):
        """Test handling single file input with non-existent file."""
        files = []
        result = self.cli._handle_single_file_input("nonexistent.pdf", files)
        assert len(result) == 0
        assert mock_print.called

    def test_handle_multiple_files_input(self):
        """Test handling multiple files input."""
        files = []
        input_str = f"{self.test_pdf1};{self.test_pdf2}"
        result = self.cli._handle_multiple_files_input(input_str, files)
        assert len(result) == 2

    @patch("builtins.print")
    def test_handle_multiple_files_input_with_nonexistent(self, mock_print):
        """Test handling multiple files with some non-existent."""
        files = []
        input_str = f"{self.test_pdf1};nonexistent.pdf"
        result = self.cli._handle_multiple_files_input(input_str, files)
        assert len(result) == 1
        assert mock_print.called

    @patch.object(CLIInterface, "_browse_files")
    @patch("builtins.print")
    def test_handle_browse_input(self, mock_print, mock_browse):
        """Test handling browse input."""
        mock_browse.return_value = [str(self.test_pdf1), str(self.test_pdf2)]
        files = []
        result = self.cli._handle_browse_input(files)
        assert len(result) == 2

    def test_handle_user_input_browse(self):
        """Test handling user input for browse."""
        with patch.object(self.cli, "_handle_browse_input") as mock_browse:
            mock_browse.return_value = ["file1.pdf"]
            files = []
            result = self.cli._handle_user_input("browse", files)
            mock_browse.assert_called_once_with(files)

    def test_handle_user_input_multiple(self):
        """Test handling user input for multiple files."""
        with patch.object(self.cli, "_handle_multiple_files_input") as mock_multiple:
            mock_multiple.return_value = ["file1.pdf", "file2.pdf"]
            files = []
            self.cli._handle_user_input("file1.pdf;file2.pdf", files)
            mock_multiple.assert_called_once_with("file1.pdf;file2.pdf", files)

    def test_handle_user_input_single(self):
        """Test handling user input for single file."""
        with patch.object(self.cli, "_handle_single_file_input") as mock_single:
            mock_single.return_value = ["file1.pdf"]
            files = []
            self.cli._handle_user_input("file1.pdf", files)
            mock_single.assert_called_once_with("file1.pdf", files)

    def test_browse_files_tkinter_unavailable(self):
        """Test browse files when tkinter is unavailable."""
        with patch("builtins.__import__", side_effect=ImportError):
            with patch("builtins.print") as mock_print:
                result = self.cli._browse_files()
                assert result == []
                assert mock_print.called

    @patch("tkinter.Tk")
    @patch("tkinter.filedialog.askopenfilenames")
    def test_browse_files_success(self, mock_dialog, mock_tk):
        """Test successful file browsing."""
        mock_root = Mock()
        mock_tk.return_value = mock_root
        mock_dialog.return_value = ["file1.pdf", "file2.pdf"]

        result = self.cli._browse_files()
        assert result == ["file1.pdf", "file2.pdf"]
        mock_root.withdraw.assert_called_once()
        mock_root.destroy.assert_called_once()

    @patch("tkinter.Tk")
    @patch("tkinter.filedialog.askopenfilenames")
    @patch("builtins.print")
    def test_browse_files_exception(self, mock_print, mock_dialog, mock_tk):
        """Test file browsing with exception."""
        mock_dialog.side_effect = Exception("Dialog error")

        result = self.cli._browse_files()
        assert result == []
        assert mock_print.called

    def test_handle_reordering_two_files(self):
        """Test reordering with only two files (should skip)."""
        files = [str(self.test_pdf1), str(self.test_pdf2)]
        result = self.cli._handle_reordering(files)
        assert result == files

    @patch.object(CLIInterface, "_ask_for_reorder")
    def test_handle_reordering_user_declines(self, mock_ask):
        """Test reordering when user declines."""
        mock_ask.return_value = False
        files = [str(self.test_pdf1), str(self.test_pdf2), str(self.test_excel1)]
        result = self.cli._handle_reordering(files)
        assert result == files

    @patch.object(CLIInterface, "_ask_for_reorder")
    @patch.object(CLIInterface, "_display_current_order")
    @patch.object(CLIInterface, "_get_new_order")
    def test_handle_reordering_user_accepts(
        self, mock_get_order, mock_display, mock_ask
    ):
        """Test reordering when user accepts."""
        mock_ask.return_value = True
        mock_get_order.return_value = ["reordered_files"]
        files = [str(self.test_pdf1), str(self.test_pdf2), str(self.test_excel1)]

        result = self.cli._handle_reordering(files)
        assert result == ["reordered_files"]
        mock_display.assert_called_once_with(files)

    def test_display_file_content_info_pdf(self):
        """Test displaying PDF file content info."""
        with patch("builtins.print") as mock_print:
            file_info = {"pages": 5}
            self.cli._display_file_content_info(file_info, "pdf")
            mock_print.assert_called_with("      Pages: 5")

    def test_display_file_content_info_excel(self):
        """Test displaying Excel file content info."""
        with patch("builtins.print") as mock_print:
            file_info = {"sheets": 3, "sheet_names": ["Sheet1", "Sheet2", "Sheet3"]}
            self.cli._display_file_content_info(file_info, "excel")
            mock_print.assert_called_with("      Sheets: 3 (Sheet1, Sheet2, Sheet3)")

    def test_display_file_content_info_excel_many_sheets(self):
        """Test displaying Excel file content info with many sheets."""
        with patch("builtins.print") as mock_print:
            file_info = {
                "sheets": 5,
                "sheet_names": ["Sheet1", "Sheet2", "Sheet3", "Sheet4", "Sheet5"],
            }
            self.cli._display_file_content_info(file_info, "excel")
            mock_print.assert_called_with("      Sheets: 5 (Sheet1, Sheet2, Sheet3...)")

    def test_handle_preview_errors_no_errors(self):
        """Test handling preview errors when there are none."""
        preview = {"errors": []}
        result = self.cli._handle_preview_errors(preview)
        assert result is False

    @patch("builtins.print")
    def test_handle_preview_errors_with_errors(self, mock_print):
        """Test handling preview errors when errors exist."""
        preview = {"errors": ["Error 1", "Error 2"]}
        result = self.cli._handle_preview_errors(preview)
        assert result is True
        assert mock_print.called

    @patch("builtins.print")
    def test_display_preview_summary(self, mock_print):
        """Test displaying preview summary."""
        preview = {
            "file_type": "pdf",
            "file_count": 2,
            "total_size_formatted": "1.5 MB",
            "estimated_output_size_formatted": "1.4 MB",
        }
        self.cli._display_preview_summary(preview)
        assert mock_print.called

    @patch("builtins.print")
    def test_display_preview_warnings_no_warnings(self, mock_print):
        """Test displaying preview warnings when there are none."""
        preview = {"warnings": []}
        self.cli._display_preview_warnings(preview)
        # Should not print warnings section
        mock_print.assert_not_called()

    @patch("builtins.print")
    def test_display_preview_warnings_with_warnings(self, mock_print):
        """Test displaying preview warnings when warnings exist."""
        preview = {"warnings": ["Warning 1", "Warning 2"]}
        self.cli._display_preview_warnings(preview)
        assert mock_print.called

    @patch.object(CLIInterface, "_handle_preview_errors")
    @patch.object(CLIInterface, "_display_preview_summary")
    @patch.object(CLIInterface, "_display_file_details")
    @patch.object(CLIInterface, "_display_preview_warnings")
    @patch("builtins.print")
    def test_show_preview(
        self, mock_print, mock_warnings, mock_details, mock_summary, mock_errors
    ):
        """Test show preview functionality."""
        mock_errors.return_value = False
        preview_data = {"file_type": "pdf"}

        with patch.object(self.cli.merger, "preview_merge", return_value=preview_data):
            files = [str(self.test_pdf1)]
            self.cli._show_preview(files)

            mock_errors.assert_called_once_with(preview_data)
            mock_summary.assert_called_once_with(preview_data)
            mock_details.assert_called_once_with(preview_data)
            mock_warnings.assert_called_once_with(preview_data)

    @patch.object(CLIInterface, "_handle_preview_errors")
    @patch("builtins.print")
    def test_show_preview_with_errors(self, mock_print, mock_errors):
        """Test show preview with errors (should return early)."""
        mock_errors.return_value = True
        preview_data = {"errors": ["Some error"]}

        with patch.object(self.cli.merger, "preview_merge", return_value=preview_data):
            files = [str(self.test_pdf1)]
            self.cli._show_preview(files)

            mock_errors.assert_called_once_with(preview_data)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_get_merge_options_pdf_yes(self, mock_print, mock_input):
        """Test getting merge options for PDF with bookmarks."""
        mock_input.return_value = "y"

        # Mock the detector to return 'pdf'
        with patch.object(self.cli.detector, "detect_file_type", return_value="pdf"):
            result = self.cli._get_merge_options()
            assert result.get("add_bookmarks") is True

    @patch("builtins.input")
    @patch("builtins.print")
    def test_get_merge_options_pdf_no(self, mock_print, mock_input):
        """Test getting merge options for PDF without bookmarks."""
        mock_input.return_value = "n"

        # Mock the detector to return 'pdf'
        with patch.object(self.cli.detector, "detect_file_type", return_value="pdf"):
            result = self.cli._get_merge_options()
            assert result.get("add_bookmarks") is False


class TestCLIInterfaceMergeOperations:
    """Test cases for CLI merge operations."""

    def setup_method(self):
        """Set up test fixtures."""
        self.cli = CLIInterface()
        self.temp_dir = tempfile.mkdtemp()

        # Create test files
        self.test_pdf1 = Path(self.temp_dir) / "test1.pdf"
        self.test_pdf2 = Path(self.temp_dir) / "test2.pdf"

        # Create dummy files
        for file_path in [self.test_pdf1, self.test_pdf2]:
            file_path.write_text("dummy content")

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch("builtins.print")
    def test_merge_files_success(self, mock_print):
        """Test successful file merge."""
        mock_result = {
            "success": True,
            "message": "Successfully merged 2 files",
            "output_file": "output.pdf",
        }

        with patch.object(self.cli.merger, "merge_files", return_value=mock_result):
            with patch.object(self.cli, "_show_preview"):
                files = [str(self.test_pdf1), str(self.test_pdf2)]
                self.cli.merge_files(files, "output.pdf")

                assert mock_print.called

    @patch("builtins.print")
    def test_merge_files_failure(self, mock_print):
        """Test failed file merge."""
        mock_result = {
            "success": False,
            "message": "Merge failed",
            "errors": ["Error 1", "Error 2"],
        }

        with patch.object(self.cli.merger, "merge_files", return_value=mock_result):
            with patch.object(self.cli, "_show_preview"):
                files = [str(self.test_pdf1), str(self.test_pdf2)]
                self.cli.merge_files(files, "output.pdf")

                assert mock_print.called

    @patch("builtins.print")
    def test_merge_files_exception(self, mock_print):
        """Test merge files with exception."""
        with patch.object(
            self.cli.merger, "merge_files", side_effect=Exception("Test error")
        ):
            with patch.object(self.cli, "_show_preview"):
                files = [str(self.test_pdf1), str(self.test_pdf2)]
                self.cli.merge_files(files, "output.pdf")

                assert mock_print.called

    @patch("builtins.print")
    def test_perform_merge_success(self, mock_print):
        """Test perform merge with success."""
        mock_result = {
            "success": True,
            "message": "Successfully merged 2 files",
            "output_file": str(self.test_pdf1),
            "warnings": [],
        }

        with patch.object(self.cli.merger, "merge_files", return_value=mock_result):
            with patch.object(self.cli.detector, "get_file_size", return_value=1024):
                with patch.object(
                    self.cli.detector, "format_file_size", return_value="1 KB"
                ):
                    files = [str(self.test_pdf1), str(self.test_pdf2)]
                    options = {"add_bookmarks": True}
                    self.cli._perform_merge(files, "output.pdf", options)

                    assert mock_print.called

    @patch("builtins.print")
    def test_perform_merge_failure(self, mock_print):
        """Test perform merge with failure."""
        mock_result = {
            "success": False,
            "message": "Merge failed",
            "errors": ["Error 1"],
            "warnings": ["Warning 1"],
        }

        with patch.object(self.cli.merger, "merge_files", return_value=mock_result):
            files = [str(self.test_pdf1), str(self.test_pdf2)]
            options = {"add_bookmarks": True}
            self.cli._perform_merge(files, "output.pdf", options)

            assert mock_print.called


class TestCLIInterfaceOutputFile:
    """Test cases for output file handling."""

    def setup_method(self):
        """Set up test fixtures."""
        self.cli = CLIInterface()
        self.temp_dir = tempfile.mkdtemp()

        # Create test files
        self.test_pdf1 = Path(self.temp_dir) / "test1.pdf"
        self.test_pdf1.write_text("dummy content")

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_get_output_file_auto_generate(self, mock_print, mock_input):
        """Test output file with auto-generation."""
        mock_input.return_value = ""  # Empty input for auto-generation

        with patch.object(self.cli.detector, "detect_file_type", return_value="pdf"):
            with patch.object(
                self.cli.merger,
                "_generate_output_filename",
                return_value="auto_output.pdf",
            ):
                files = [str(self.test_pdf1)]
                result = self.cli._get_output_file(files)
                assert result == "auto_output.pdf"

    @patch("builtins.input")
    @patch("builtins.print")
    def test_get_output_file_directory_path(self, mock_print, mock_input):
        """Test output file with directory path."""
        mock_input.return_value = self.temp_dir

        with patch.object(self.cli.detector, "detect_file_type", return_value="pdf"):
            with patch.object(
                self.cli.merger,
                "_generate_output_filename",
                return_value="dir_output.pdf",
            ):
                files = [str(self.test_pdf1)]
                result = self.cli._get_output_file(files)
                assert result == "dir_output.pdf"

    @patch("builtins.input")
    @patch("builtins.print")
    def test_get_output_file_full_path(self, mock_print, mock_input):
        """Test output file with full path."""
        output_file = Path(self.temp_dir) / "custom_output.pdf"
        mock_input.return_value = str(output_file)

        with patch.object(self.cli.detector, "detect_file_type", return_value="pdf"):
            files = [str(self.test_pdf1)]
            result = self.cli._get_output_file(files)
            assert Path(result).name == "custom_output.pdf"

    @patch("builtins.input")
    @patch("builtins.print")
    def test_get_output_file_create_directory(self, mock_print, mock_input):
        """Test output file with non-existent directory creation."""
        new_dir = Path(self.temp_dir) / "new_dir" / "output.pdf"
        mock_input.side_effect = [str(new_dir), "y"]  # Path, then yes to create

        with patch.object(self.cli.detector, "detect_file_type", return_value="pdf"):
            files = [str(self.test_pdf1)]
            result = self.cli._get_output_file(files)
            assert Path(result).name == "output.pdf"

    @patch("builtins.input")
    @patch("builtins.print")
    def test_get_output_file_reject_directory_creation(self, mock_print, mock_input):
        """Test output file when user rejects directory creation."""
        new_dir = Path(self.temp_dir) / "new_dir" / "output.pdf"
        existing_file = Path(self.temp_dir) / "existing.pdf"
        mock_input.side_effect = [
            str(new_dir),
            "n",
            str(existing_file),
        ]  # Path, no to create, then existing path

        with patch.object(self.cli.detector, "detect_file_type", return_value="pdf"):
            files = [str(self.test_pdf1)]
            result = self.cli._get_output_file(files)
            assert Path(result).name == "existing.pdf"


class TestCLIInterfaceGetNewOrder:
    """Test cases for getting new file order."""

    def setup_method(self):
        """Set up test fixtures."""
        self.cli = CLIInterface()
        self.temp_dir = tempfile.mkdtemp()

        # Create test files
        self.test_files = []
        for i in range(3):
            file_path = Path(self.temp_dir) / f"test{i}.pdf"
            file_path.write_text("dummy content")
            self.test_files.append(str(file_path))

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_get_new_order_success(self, mock_print, mock_input):
        """Test successful new order input."""
        mock_input.side_effect = ["2 1 3", "y"]  # New order, then confirm

        with patch.object(self.cli.merger, "reorder_files", return_value=["reordered"]):
            result = self.cli._get_new_order(self.test_files)
            assert result == ["reordered"]

    @patch("builtins.input")
    @patch("builtins.print")
    def test_get_new_order_reject_then_accept(self, mock_print, mock_input):
        """Test rejecting then accepting new order."""
        mock_input.side_effect = [
            "2 1 3",
            "n",
            "3 2 1",
            "y",
        ]  # Order, reject, new order, accept

        with patch.object(self.cli.merger, "reorder_files", return_value=["reordered"]):
            result = self.cli._get_new_order(self.test_files)
            assert result == ["reordered"]

    @patch("builtins.input")
    @patch("builtins.print")
    def test_get_new_order_invalid_numbers(self, mock_print, mock_input):
        """Test invalid number input."""
        mock_input.side_effect = [
            "invalid",
            "2 1 3",
            "y",
        ]  # Invalid, then valid order, accept

        with patch.object(self.cli.merger, "reorder_files", return_value=["reordered"]):
            result = self.cli._get_new_order(self.test_files)
            assert result == ["reordered"]

    @patch("builtins.input")
    @patch("builtins.print")
    def test_get_new_order_wrong_length(self, mock_print, mock_input):
        """Test wrong length order input."""
        mock_input.side_effect = [
            "1 2",
            "2 1 3",
            "y",
        ]  # Too short, then correct, accept

        with patch.object(self.cli.merger, "reorder_files", return_value=["reordered"]):
            with patch.object(self.cli, "_validate_order", side_effect=[False, True]):
                result = self.cli._get_new_order(self.test_files)
                assert result == ["reordered"]

    @patch("builtins.input")
    @patch("builtins.print")
    def test_get_new_order_exception(self, mock_print, mock_input):
        """Test exception during order processing."""
        # First input causes exception, second input succeeds
        mock_input.side_effect = ["2 1 3", "2 1 3", "y"]

        # First call raises exception, second call succeeds
        with patch.object(
            self.cli.merger,
            "reorder_files",
            side_effect=[Exception("Test error"), ["reordered"]],
        ):
            result = self.cli._get_new_order(self.test_files)
            assert result == ["reordered"]
            # Verify error message was printed
            mock_print.assert_any_call("Error: Test error")
