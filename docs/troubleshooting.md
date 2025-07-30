# Troubleshooting Guide

This guide helps you resolve common issues when using Document Merger.

## Installation Issues

### Python Version Error
**Error:** `Python 3.7 or higher is required`

**Solution:**
1. Check your Python version: `python --version`
2. Install Python 3.7+ from [python.org](https://python.org)
3. Ensure Python is in your system PATH
4. On Windows, use `py -3` if multiple Python versions are installed

### pip Installation Failed
**Error:** `pip install failed` or `No module named pip`

**Solutions:**
- **Windows:** `python -m ensurepip --upgrade`
- **macOS:** `python3 -m ensurepip --upgrade`
- **Linux:** `sudo apt-get install python3-pip`

### Virtual Environment Issues
**Error:** Virtual environment activation fails

**Solutions:**
```bash
# Windows PowerShell (if execution policy blocks)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Alternative activation methods
# Windows Command Prompt:
document_merger_env\Scripts\activate.bat

# Windows PowerShell:
document_merger_env\Scripts\Activate.ps1
```

## PyPDF2 Issues

### Bookmark Deprecation Warning
**Warning:** `PendingDeprecationWarning: bookmark is deprecated`

**Solution:** This is already fixed in the current version. Update to latest:
```bash
git pull origin main
pip install -r requirements.txt
```

### PDF Corruption Errors
**Error:** `PyPDF2.errors.PdfReadError: Invalid PDF header`

**Solutions:**
1. **Verify PDF files:** Open PDFs in a PDF viewer to confirm they're valid
2. **Re-download files:** Source files may be corrupted during download
3. **Convert format:** Use online tools to repair/convert problematic PDFs
4. **Check file extensions:** Ensure files have `.pdf` extension

### Password Protected PDFs
**Error:** `File has not been decrypted`

**Solutions:**
1. **Remove password protection** using PDF software before merging
2. **Use command line tools:**
   ```bash
   # Using qpdf (install separately)
   qpdf --password=yourpassword --decrypt input.pdf output.pdf
   ```

## Excel/openpyxl Issues

### File Format Errors
**Error:** `zipfile.BadZipFile: File is not a zip file`

**Solutions:**
1. **Check file format:** Ensure files are `.xlsx` (not `.xls` or other formats)
2. **Convert format:** Open in Excel and save as `.xlsx`
3. **Verify file integrity:** Re-download if files are corrupted

### Memory Issues with Large Files
**Error:** `MemoryError` or system becomes unresponsive

**Solutions:**
1. **Process smaller batches:**
   ```python
   # Split large operations
   files_batch1 = files[:5]
   files_batch2 = files[5:]
   ```
2. **Close other applications** to free memory
3. **Use 64-bit Python** for better memory handling
4. **Consider file size limits:** Excel has ~1M row limit

## GUI Issues

### Tkinter Import Error
**Error:** `No module named 'tkinter'`

**Solutions:**
- **Windows:** Reinstall Python with "tcl/tk and IDLE" option checked
- **Ubuntu/Debian:** `sudo apt-get install python3-tk`
- **CentOS/RHEL:** `sudo yum install tkinter`
- **macOS:** Usually included; try `python3 -m tkinter`

### GUI Won't Start
**Error:** GUI window doesn't appear

**Solutions:**
1. **Check display settings** (especially on remote systems)
2. **Try CLI version** as alternative:
   ```bash
   python -m src.cli.cli_interface --help
   ```
3. **Verify tkinter installation:**
   ```python
   python -c "import tkinter; print('tkinter works')"
   ```

### Files Not Showing in File Picker
**Issue:** File dialog doesn't show expected files

**Solutions:**
1. **Check file extensions:** Ensure correct file types (.pdf, .xlsx)
2. **Navigate to correct folder** using the file dialog
3. **Check file permissions** (ensure read access)
4. **Refresh folder view** or restart application

## CLI Issues

### Command Not Found
**Error:** `python: command not found` or module errors

**Solutions:**
1. **Use full Python path:**
   ```bash
   # Windows
   C:\Python39\python.exe -m src.cli.cli_interface
   
   # macOS/Linux  
   /usr/bin/python3 -m src.cli.cli_interface
   ```
2. **Activate virtual environment first:**
   ```bash
   document_merger_env\Scripts\activate  # Windows
   source document_merger_env/bin/activate  # macOS/Linux
   ```

### Module Import Errors
**Error:** `ModuleNotFoundError: No module named 'src'`

**Solutions:**
1. **Run from project root directory:**
   ```bash
   cd document-merger
   python -m src.cli.cli_interface
   ```
2. **Check PYTHONPATH:**
   ```bash
   # Add current directory to Python path
   export PYTHONPATH="${PYTHONPATH}:."  # Linux/macOS
   set PYTHONPATH=%PYTHONPATH%;.        # Windows
   ```

## File System Issues

### Permission Denied
**Error:** `PermissionError: [Errno 13] Permission denied`

**Solutions:**
1. **Check file permissions:** Ensure write access to output directory
2. **Close files in other applications** (Excel, PDF readers)
3. **Run with elevated permissions** if necessary:
   ```bash
   # Windows (as Administrator)
   # macOS/Linux
   sudo python main.py
   ```
4. **Choose different output location** with write access

### Disk Space Issues
**Error:** `OSError: [Errno 28] No space left on device`

**Solutions:**
1. **Check available disk space:**
   ```bash
   # Windows
   dir C:\
   
   # macOS/Linux
   df -h
   ```
2. **Clean temporary files:**
   ```bash
   # Windows
   del /s /q %TEMP%\*
   
   # macOS/Linux
   rm -rf /tmp/*
   ```
3. **Use different output drive** with more space
4. **Process files in smaller batches**

## Performance Issues

### Slow Processing
**Issue:** File processing takes very long

**Solutions:**
1. **Check file sizes:** Large files naturally take longer
2. **Close background applications** to free resources
3. **Use SSD storage** for better I/O performance
4. **Process in batches** for very large operations
5. **Monitor system resources:**
   ```bash
   # Windows
   taskmgr
   
   # macOS
   Activity Monitor
   
   # Linux
   htop
   ```

### Memory Usage
**Issue:** High memory consumption

**Solutions:**
1. **Monitor memory usage** during operations
2. **Restart application** between large operations
3. **Increase virtual memory/swap space**
4. **Use CLI interface** for better memory efficiency

## Common Workflow Issues

### Wrong File Order
**Issue:** Merged files are in wrong order

**Solutions:**
1. **GUI:** Drag and drop to reorder files
2. **CLI:** Specify files in correct order in command
3. **Use numbered filenames** for natural sorting
4. **Double-check file list** before merging

### Missing Files in Output
**Issue:** Some files don't appear in merged output

**Solutions:**
1. **Check error messages** in console/logs
2. **Validate all input files** before merging
3. **Verify file permissions** and accessibility
4. **Try merging problematic files separately**

### Output File Corruption
**Issue:** Merged file won't open or is corrupted

**Solutions:**
1. **Validate input files** first
2. **Check available disk space** during operation
3. **Ensure output directory** has write permissions
4. **Try different output location**
5. **Merge smaller batches** to isolate problematic files

## Getting Additional Help

### Enable Debug Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
# Run your operation to see detailed logs
```

### Create Minimal Test Case
```python
# Test with simple files first
from src.core.pdf_merger import PDFMerger

merger = PDFMerger()
result = merger.merge_pdfs(["simple1.pdf", "simple2.pdf"], "test_output.pdf")
print(f"Test result: {result}")
```

### System Information
When reporting issues, include:
```bash
# System info
python --version
pip list
# Operating system and version
# File sizes and types
# Error messages (full traceback)
```

### Contact Support
- **GitHub Issues:** [Create an issue](https://github.com/your-username/document-merger/issues)
- **Documentation:** Check [README.md](../README.md) and [examples](examples/)
- **API Reference:** Review [API documentation](api/README.md)

## Prevention Tips

1. **Test with small files first**
2. **Keep backups of original files**
3. **Update dependencies regularly**
4. **Monitor system resources during operations**
5. **Use version control for your documents**
6. **Validate files before batch operations**
