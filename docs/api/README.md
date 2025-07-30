# API Documentation

This directory contains detailed API documentation for Document Merger's core modules.

## Core Modules

### PDF Processing
- [`PDFMerger`](pdf_merger.md) - Main PDF merging functionality
- [`PDFProcessor`](pdf_processor.md) - Low-level PDF operations

### Excel Processing  
- [`ExcelMerger`](excel_merger.md) - Excel file merging capabilities
- [`SheetProcessor`](sheet_processor.md) - Individual worksheet operations

### User Interfaces
- [`GUIInterface`](gui_interface.md) - Tkinter-based graphical interface
- [`CLIInterface`](cli_interface.md) - Command-line interface

### Utilities
- [`FileHandler`](file_handler.md) - File system operations
- [`ValidationUtils`](validation_utils.md) - Input validation and error handling

## Quick Reference

### PDF Merging
```python
from src.core.pdf_merger import PDFMerger

merger = PDFMerger()
merger.add_file("file1.pdf", outline_item="Chapter 1")
merger.add_file("file2.pdf", outline_item="Chapter 2")
merger.merge("output.pdf")
```

### Excel Merging
```python
from src.core.excel_merger import ExcelMerger

merger = ExcelMerger()
merger.add_file("data1.xlsx")
merger.add_file("data2.xlsx") 
merger.merge("combined.xlsx")
```

## Error Handling

All modules include comprehensive error handling:
- Input validation
- File existence checks
- Permission verification
- Memory management
- Graceful failure recovery

## Threading and Performance

- GUI operations run in separate threads
- Large file processing includes progress callbacks
- Memory usage is optimized for large documents
- Batch processing capabilities available

## Extensions and Customization

The modular design allows for easy extension:
- Custom file processors
- Additional output formats
- Custom validation rules
- Plugin architecture ready

## Version Compatibility

- Python 3.7+ required
- PyPDF2 3.0+ for updated API
- Tkinter included with Python
- Cross-platform compatibility (Windows, macOS, Linux)
