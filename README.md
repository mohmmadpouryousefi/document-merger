# Document Merger

A comprehensive Python application for merging PDF and Excel files with both GUI and CLI interfaces.

##  Features

- **PDF Merging**: Merge multiple PDF files while preserving layout, fonts, and images
- **Excel Merging**: Combine Excel files into separate sheets with formatting preservation
- **Dual Interface**: Both graphical (GUI) and command-line (CLI) interfaces
- **File Validation**: Automatic file type detection and corruption checking
- **Error Handling**: Comprehensive error management and user feedback
- **Cross-Platform**: Windows, macOS, and Linux support

##  Quick Start

### Installation
```bash
# Clone the repository
git clone https://github.com/mohmmadpouryousefi/document-merger.git
cd document-merger

# Install dependencies
pip install -r requirements.txt

# Run setup (optional)
python setup.py
```

### Usage

#### GUI Mode (Recommended)
```bash
python main.py
```

#### CLI Mode
```bash
# Interactive mode
python main.py --cli

# Direct usage
python main.py --cli --files file1.pdf file2.pdf --output merged.pdf

# Help
python main.py --help
```

##  Project Structure

```
document-merger/
 main.py                 # Main application entry point
 requirements.txt        # Python dependencies
 setup.py               # Installation script
 .gitignore             # Git ignore rules
 README.md              # This file

 src/                   # Source code
    core/             # Core functionality
       file_detector.py    # File type detection
       file_merger.py      # Main merger orchestrator
       pdf_merger.py       # PDF merging logic
       excel_merger.py     # Excel merging logic
    gui/              # Graphical interface
       main_window.py      # GUI implementation
    cli/              # Command line interface
        cli_interface.py    # CLI implementation

 docs/                 # Documentation (coming soon)
```

##  Requirements

- **Python**: 3.7 or higher
- **Dependencies**:
  - PyPDF2 (PDF operations)
  - openpyxl (Excel operations)
  - tkinter (GUI - included with Python)
  - Pillow (Image processing)

##  Supported Formats

### PDF Files
- **Input**: `.pdf` files
- **Features**: Layout preservation, bookmark creation, metadata handling

### Excel Files
- **Input**: `.xlsx`, `.xls`, `.xlsm` files
- **Features**: Multi-sheet merging, formula preservation, formatting retention

##  Development

### Testing
```bash
# Run installation test
python test_installation.py

# Run bookmark fix test
python test_bookmark_fix.py
```

### Features in Development
- Additional file format support
- Cloud storage integration
- Advanced PDF features
- Performance optimizations

##  Known Issues & Fixes

### Recent Fixes
-  **PDF Bookmark Issue**: Fixed PyPDF2 deprecation warning by updating from `bookmark` to `outline_item` parameter

##  Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

##  License

This project is open source and available under the MIT License.

##  Version History

- **v1.0.0**: Initial release with full PDF and Excel merging capabilities
- **v1.0.1**: Fixed PyPDF2 bookmark deprecation warnings

##  Author

**Mohammad Pouryousefi**
- GitHub: [@mohmmadpouryousefi](https://github.com/mohmmadpouryousefi)

---

*Built with  for document management automation*
