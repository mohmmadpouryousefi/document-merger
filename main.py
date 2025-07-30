"""
File Merger Application

A Python application that merges multiple files of the same type (PDF or Excel)
into a single output file with support for both GUI and CLI interfaces.

Features:
- Automatic file type detection
- PDF merging with layout preservation
- Excel merging with multiple sheets
- User-friendly interface options
- Error handling for corrupted/unsupported files
- File reordering capability
- Extensible architecture for future formats

Usage:
    python main.py                  # Launch GUI
    python main.py --cli            # Use CLI interface
    python main.py --help           # Show help
"""

import argparse

from src.cli.cli_interface import CLIInterface
from src.gui.main_window import FileManagerGUI


def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(
        description="Merge multiple files of the same type (PDF or Excel)"
    )
    parser.add_argument(
        "--cli", action="store_true", help="Use command line interface instead of GUI"
    )
    parser.add_argument(
        "--files", nargs="+", help="Input files to merge (CLI mode only)"
    )
    parser.add_argument("--output", help="Output file path (CLI mode only)")

    args = parser.parse_args()

    if args.cli:
        # Use CLI interface
        cli = CLIInterface()
        if args.files and args.output:
            cli.merge_files(args.files, args.output)
        else:
            cli.interactive_mode()
    else:
        # Use GUI interface
        app = FileManagerGUI()
        app.run()


if __name__ == "__main__":
    main()
