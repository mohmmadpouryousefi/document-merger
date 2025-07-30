# File Merger Application - Project Structure

## Overview
This is a comprehensive Python application for merging PDF and Excel files with both GUI and CLI interfaces.

## Project Structure
```
file-merger/
├── main.py                     # Main application entry point
├── setup.py                   # Installation script
├── test_installation.py       # Installation test script
├── run.bat                    # Windows launcher script
├── requirements.txt           # Python dependencies
├── README.md                  # Documentation
├── file_merger.log           # Application log file (created at runtime)
│
├── src/                      # Source code directory
│   ├── __init__.py
│   │
│   ├── core/                 # Core functionality modules
│   │   ├── __init__.py
│   │   ├── config.py         # Configuration settings
│   │   ├── file_detector.py  # File type detection and validation
│   │   ├── file_merger.py    # Main merger orchestrator
│   │   ├── pdf_merger.py     # PDF-specific merging logic
│   │   └── excel_merger.py   # Excel-specific merging logic
│   │
│   ├── gui/                  # Graphical User Interface
│   │   ├── __init__.py
│   │   └── main_window.py    # Main GUI window implementation
│   │
│   └── cli/                  # Command Line Interface
│       ├── __init__.py
│       └── cli_interface.py  # CLI implementation
│
├── sample_files/             # Sample files for testing (created at runtime)
│   ├── test_file.txt
│   └── README.txt
│
└── .venv/                    # Virtual environment (created automatically)
    └── Scripts/
        └── python.exe
```

## Key Features Implemented

### 1. File Type Detection (`file_detector.py`)
- Automatic detection of PDF and Excel files
- Support for multiple Excel formats (.xlsx, .xls, .xlsm)
- File validation and corruption detection
- File size calculation and formatting
- Accessibility checking

### 2. PDF Merging (`pdf_merger.py`)
- Merges multiple PDF files while preserving layout, fonts, and images
- Optional bookmark creation for each merged file
- PDF validation and metadata extraction
- Support for encrypted PDFs (where permitted)

### 3. Excel Merging (`excel_merger.py`)
- Merges multiple Excel files into separate sheets
- Preserves all formatting, formulas, and styles
- Handles merged cells, column/row dimensions
- Copies sheet properties and print settings
- Supports specific sheet selection for advanced users

### 4. Main Orchestrator (`file_merger.py`)
- Coordinates different file type mergers
- Comprehensive error handling and logging
- File preview functionality
- Auto-generated output filenames
- Operation status reporting

### 5. GUI Interface (`main_window.py`)
- User-friendly drag-and-drop interface
- File list management with reordering capabilities
- Real-time file information display
- Preview functionality before merging
- Progress tracking during operations
- File validation and error reporting

### 6. CLI Interface (`cli_interface.py`)
- Interactive command-line mode
- Batch processing capabilities
- File browsing support (where available)
- Step-by-step guided merging
- Direct command-line arguments support

## Usage Examples

### GUI Mode
```bash
python main.py
```
or double-click `run.bat`

### CLI Interactive Mode
```bash
python main.py --cli
```

### CLI Direct Mode
```bash
python main.py --cli --files file1.pdf file2.pdf --output merged.pdf
```

### Help
```bash
python main.py --help
```

## Configuration Options

The application includes comprehensive configuration options in `config.py`:
- File size limits
- Supported file extensions
- Default paths and directories
- Performance settings
- Logging configuration
- Format-specific options

## Error Handling

The application includes robust error handling for:
- Missing or inaccessible files
- Corrupted file formats
- Memory and disk space issues
- Permission problems
- Network drive access issues

## Testing

Run the installation test to verify everything is working:
```bash
python test_installation.py
```

## Dependencies

- **PyPDF2**: PDF file manipulation
- **openpyxl**: Excel file handling
- **tkinter**: GUI framework (included with Python)
- **Pillow**: Image processing support
- **pathlib**: Modern path handling

## Extensibility

The application is designed to be easily extensible for additional file formats:

1. Create a new merger class (e.g., `word_merger.py`)
2. Add detection logic to `file_detector.py`
3. Update the main orchestrator in `file_merger.py`
4. Add UI elements as needed

## Performance Notes

- **PDF merging**: ~1-2 seconds per MB
- **Excel merging**: ~2-3 seconds per sheet
- **Memory usage**: Base ~50-100MB + 2x largest file size
- **Recommended limits**: <50 files or <500MB total per operation

## Support

For issues or questions:
1. Check the application log file (`file_merger.log`)
2. Run the test script (`python test_installation.py`)
3. Use preview functionality to identify problems before merging
4. Try processing files in smaller batches for large operations

## Version
Current version: 1.0.0
Release date: 2024
