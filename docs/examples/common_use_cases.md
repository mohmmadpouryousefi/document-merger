# Common Use Cases

This guide covers the most common scenarios for using Document Merger.

## PDF Use Cases

### 1. Merging Multiple Reports
**Scenario:** You have several PDF reports that need to be combined into one document.

**Solution:**
1. Open Document Merger GUI
2. Click "Add Files" and select all PDF reports
3. Ensure files are in the correct order (drag to reorder if needed)
4. Choose "Add bookmarks" to create navigation
5. Click "Merge Files" and save as "Combined_Report.pdf"

**CLI Alternative:**
```bash
python -m src.cli.cli_interface --type pdf --files report1.pdf report2.pdf report3.pdf --output combined_report.pdf --bookmarks
```

### 2. Creating a Document Package
**Scenario:** Combine contracts, invoices, and supporting documents for a client.

**Steps:**
1. Organize files in logical order
2. Use bookmark feature to create sections
3. Name bookmarks descriptively (e.g., "Contract", "Invoice #001")
4. Merge with preservation of original formatting

### 3. Academic Paper Compilation
**Scenario:** Combine research papers, appendices, and references.

**Best Practices:**
- Add bookmarks for each paper/section
- Maintain original page numbering
- Include table of contents as first page

## Excel Use Cases

### 1. Monthly Data Consolidation
**Scenario:** Combine monthly sales data from multiple Excel files.

**Solution:**
1. Select all monthly Excel files
2. Choose "Merge all sheets" option
3. Use "Preserve sheet names" to maintain monthly labels
4. Save as "Annual_Sales_Data.xlsx"

**CLI Alternative:**
```bash
python -m src.cli.cli_interface --type excel --files jan.xlsx feb.xlsx mar.xlsx --output quarterly.xlsx
```

### 2. Department Budget Compilation
**Scenario:** Each department submits budget in separate Excel file.

**Steps:**
1. Collect all department Excel files
2. Merge with sheet name preservation
3. Each department becomes a separate worksheet
4. Create summary sheet manually if needed

### 3. Survey Data Aggregation
**Scenario:** Multiple survey response files need combining.

**Approach:**
- Use GUI for visual verification
- Check data alignment before merging
- Verify column headers match across files

## Automation Use Cases

### 1. Daily Report Generation
**Scenario:** Automatically merge daily files into weekly reports.

**Script Example:**
```python
from src.core.pdf_merger import PDFMerger
import os
from datetime import datetime, timedelta

def create_weekly_report():
    merger = PDFMerger()
    
    # Get files from last 7 days
    for i in range(7):
        date = datetime.now() - timedelta(days=i)
        filename = f"daily_report_{date.strftime('%Y%m%d')}.pdf"
        if os.path.exists(filename):
            merger.add_file(filename, outline_item=f"Day {i+1}")
    
    merger.merge("weekly_report.pdf")
```

### 2. Batch Processing
**Scenario:** Process multiple document sets with same structure.

**PowerShell Script:**
```powershell
# Batch merge multiple document sets
$folders = Get-ChildItem -Directory
foreach ($folder in $folders) {
    $files = Get-ChildItem -Path $folder.FullName -Filter "*.pdf"
    $output = "$($folder.Name)_merged.pdf"
    python -m src.cli.cli_interface --type pdf --files $files --output $output
}
```

## Tips for Success

### File Organization
- Keep source files organized in folders
- Use consistent naming conventions
- Backup original files before processing

### Performance Optimization
- For large files, use CLI interface for better performance
- Process files in smaller batches if memory is limited
- Close other applications during large operations

### Quality Assurance
- Always verify merged output
- Check bookmark navigation (for PDFs)
- Verify data integrity (for Excel files)
- Test with small samples first

## Troubleshooting Common Issues

### PDF Issues
- **Corrupted bookmarks:** Ensure source PDFs are valid
- **Large file sizes:** Consider PDF optimization tools
- **Password protected files:** Remove protection before merging

### Excel Issues
- **Formula errors:** Formulas may need manual adjustment
- **Formatting loss:** Some complex formatting may not preserve
- **Memory issues:** Split large datasets into smaller files

### General Issues
- **Slow performance:** Check available disk space and memory
- **Permission errors:** Ensure write access to output directory
- **File not found:** Verify file paths and names

## Getting Help

If your use case isn't covered here:
1. Check the [API Documentation](../api/README.md)
2. Review [Troubleshooting Guide](../troubleshooting.md)
3. Look at [Python API Examples](python_api_examples.md)
4. Create an issue on GitHub for complex scenarios
