# PDFMerger API Documentation

The `PDFMerger` class provides comprehensive PDF merging capabilities with support for bookmarks, metadata preservation, and validation.

## Class: PDFMerger

### Overview
```python
from src.core.pdf_merger import PDFMerger

merger = PDFMerger()
```

The PDFMerger class handles merging of PDF files while preserving layout, fonts, images, and optional bookmark creation.

## Methods

### `__init__()`
Initialize the PDF merger.

```python
merger = PDFMerger()
```

**Parameters:** None

**Returns:** PDFMerger instance

---

### `merge_pdfs(input_files, output_file)`
Merge multiple PDF files into a single PDF.

```python
success = merger.merge_pdfs(
    input_files=["file1.pdf", "file2.pdf", "file3.pdf"],
    output_file="merged_output.pdf"
)
```

**Parameters:**
- `input_files` (List[str]): List of input PDF file paths
- `output_file` (str): Output PDF file path

**Returns:** 
- `bool`: True if successful, False otherwise

**Raises:**
- `Exception`: If any PDF file cannot be processed

**Example:**
```python
merger = PDFMerger()
files = ["report1.pdf", "report2.pdf", "appendix.pdf"]
result = merger.merge_pdfs(files, "combined_report.pdf")
if result:
    print("PDF merge successful!")
else:
    print("PDF merge failed!")
```

---

### `merge_with_bookmarks(input_files, output_file)`
Merge PDFs while preserving existing bookmarks and adding file-based bookmarks.

```python
success = merger.merge_with_bookmarks(
    input_files=["chapter1.pdf", "chapter2.pdf"],
    output_file="book.pdf"
)
```

**Parameters:**
- `input_files` (List[str]): List of input PDF file paths
- `output_file` (str): Output PDF file path

**Returns:** 
- `bool`: True if successful, False otherwise

**Features:**
- Preserves existing bookmarks from source PDFs
- Creates new bookmarks for each merged file
- Uses filename as bookmark title
- Maintains proper bookmark hierarchy

**Example:**
```python
merger = PDFMerger()
chapters = ["intro.pdf", "methodology.pdf", "results.pdf", "conclusion.pdf"]
result = merger.merge_with_bookmarks(chapters, "thesis.pdf")
# Creates bookmarks: "File 1: intro", "File 2: methodology", etc.
```

---

### `validate_pdf(file_path)`
Validate if a PDF file is readable and not corrupted.

```python
is_valid = merger.validate_pdf("document.pdf")
```

**Parameters:**
- `file_path` (str): Path to the PDF file

**Returns:** 
- `bool`: True if valid, False if corrupted or unreadable

**Example:**
```python
merger = PDFMerger()
files = ["doc1.pdf", "doc2.pdf", "doc3.pdf"]
valid_files = [f for f in files if merger.validate_pdf(f)]
print(f"Valid files: {len(valid_files)}/{len(files)}")
```

---

### `get_pdf_info(file_path)`
Get detailed information about a PDF file.

```python
info = merger.get_pdf_info("document.pdf")
```

**Parameters:**
- `file_path` (str): Path to the PDF file

**Returns:** 
- `dict`: Dictionary containing PDF metadata and properties

**Return Dictionary Keys:**
- `pages` (int): Number of pages
- `title` (str or None): Document title
- `author` (str or None): Document author  
- `subject` (str or None): Document subject
- `creator` (str or None): Document creator application
- `encrypted` (bool): Whether PDF is password protected
- `error` (str): Error message if file cannot be read

**Example:**
```python
merger = PDFMerger()
info = merger.get_pdf_info("report.pdf")

print(f"Pages: {info['pages']}")
print(f"Title: {info['title']}")
print(f"Author: {info['author']}")
print(f"Encrypted: {info['encrypted']}")

if 'error' in info:
    print(f"Error reading PDF: {info['error']}")
```

## Error Handling

All methods include comprehensive error handling:

- **File Access Errors**: Handles missing files, permission issues
- **PDF Corruption**: Detects and reports corrupted PDF files
- **Memory Issues**: Manages memory for large PDF files
- **Output Directory**: Creates output directories if they don't exist

### Exception Types

```python
try:
    merger.merge_pdfs(files, output)
except Exception as e:
    # Handle specific error types
    if "Failed to process" in str(e):
        print("PDF file corruption detected")
    elif "Permission denied" in str(e):
        print("File access permission error")
    else:
        print(f"Unexpected error: {e}")
```

## Best Practices

### 1. Validate Files First
```python
merger = PDFMerger()
files = ["file1.pdf", "file2.pdf"]

# Validate all files before merging
valid_files = []
for file in files:
    if merger.validate_pdf(file):
        valid_files.append(file)
    else:
        print(f"Skipping invalid file: {file}")

if valid_files:
    merger.merge_pdfs(valid_files, "output.pdf")
```

### 2. Check File Information
```python
merger = PDFMerger()
total_pages = 0

for file in files:
    info = merger.get_pdf_info(file)
    total_pages += info['pages']
    print(f"{file}: {info['pages']} pages")

print(f"Total pages in merged PDF: {total_pages}")
```

### 3. Handle Large Files
```python
import os

merger = PDFMerger()
files = ["large1.pdf", "large2.pdf"]

# Check available disk space
output_size_estimate = sum(os.path.getsize(f) for f in files)
print(f"Estimated output size: {output_size_estimate / (1024*1024):.1f} MB")

# Process in chunks if needed
if len(files) > 10:
    # Process in batches
    for i in range(0, len(files), 5):
        batch = files[i:i+5]
        merger.merge_pdfs(batch, f"batch_{i//5}.pdf")
```

## Performance Considerations

- **Memory Usage**: Large PDFs are processed efficiently with streaming
- **Disk Space**: Ensure adequate space for output files
- **Processing Time**: Time scales with total page count and file sizes
- **Concurrent Processing**: Single-threaded for thread safety

## Dependencies

- **PyPDF2 >= 3.0.1**: Core PDF processing library
- **pathlib**: Path manipulation (Python standard library)
- **logging**: Error and info logging (Python standard library)

## Thread Safety

The PDFMerger class is **not thread-safe**. Create separate instances for concurrent operations:

```python
import threading

def merge_worker(files, output):
    merger = PDFMerger()  # Separate instance per thread
    merger.merge_pdfs(files, output)

# Safe concurrent usage
thread1 = threading.Thread(target=merge_worker, args=(files1, "output1.pdf"))
thread2 = threading.Thread(target=merge_worker, args=(files2, "output2.pdf"))
```

## Version History

- **v1.0**: Initial implementation with basic merging
- **v1.1**: Added bookmark support and validation
- **v1.2**: Fixed PyPDF2 3.0+ compatibility (outline_item parameter)
- **v1.3**: Enhanced error handling and metadata preservation
