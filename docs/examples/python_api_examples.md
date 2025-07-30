# Python API Examples

This guide shows how to use Document Merger's core modules programmatically in your Python scripts.

## Basic PDF Merging

### Simple PDF Merge
```python
from src.core.pdf_merger import PDFMerger

def simple_pdf_merge():
    """Basic PDF merging example."""
    merger = PDFMerger()

    # List of PDF files to merge
    pdf_files = [
        "document1.pdf",
        "document2.pdf",
        "document3.pdf"
    ]

    # Merge files
    success = merger.merge_pdfs(pdf_files, "merged_output.pdf")

    if success:
        print("✓ PDF merge completed successfully")
    else:
        print("✗ PDF merge failed")

# Run the example
simple_pdf_merge()
```

### PDF Merge with Validation
```python
from src.core.pdf_merger import PDFMerger
import os

def validated_pdf_merge():
    """PDF merging with pre-validation."""
    merger = PDFMerger()

    # Input files (some may be invalid)
    candidate_files = [
        "good_file.pdf",
        "corrupted_file.pdf",  # This might be invalid
        "another_good_file.pdf"
    ]

    # Validate files first
    valid_files = []
    for file_path in candidate_files:
        if os.path.exists(file_path):
            if merger.validate_pdf(file_path):
                valid_files.append(file_path)
                print(f"✓ Valid: {file_path}")
            else:
                print(f"✗ Invalid: {file_path}")
        else:
            print(f"✗ Not found: {file_path}")

    # Merge only valid files
    if valid_files:
        success = merger.merge_pdfs(valid_files, "validated_output.pdf")
        print(f"Merged {len(valid_files)} valid files")
    else:
        print("No valid files to merge")

validated_pdf_merge()
```

### PDF Merge with Bookmarks
```python
from src.core.pdf_merger import PDFMerger

def pdf_merge_with_bookmarks():
    """Create a merged PDF with bookmarks for navigation."""
    merger = PDFMerger()

    # Files representing different sections
    section_files = [
        "introduction.pdf",
        "methodology.pdf",
        "results.pdf",
        "conclusion.pdf"
    ]

    # Merge with automatic bookmark creation
    success = merger.merge_with_bookmarks(section_files, "complete_document.pdf")

    if success:
        print("✓ PDF merged with bookmarks")
        print("Bookmarks created for each section")
    else:
        print("✗ Bookmark merge failed")

pdf_merge_with_bookmarks()
```

## Advanced PDF Operations

### PDF Information Extraction
```python
from src.core.pdf_merger import PDFMerger
import json

def analyze_pdf_collection():
    """Analyze a collection of PDF files."""
    merger = PDFMerger()

    pdf_files = [
        "report1.pdf",
        "report2.pdf",
        "appendix.pdf"
    ]

    collection_info = {}
    total_pages = 0

    for pdf_file in pdf_files:
        info = merger.get_pdf_info(pdf_file)
        collection_info[pdf_file] = info
        total_pages += info.get('pages', 0)

        print(f"\n📄 {pdf_file}:")
        print(f"   Pages: {info.get('pages', 'Unknown')}")
        print(f"   Title: {info.get('title', 'No title')}")
        print(f"   Author: {info.get('author', 'No author')}")
        print(f"   Encrypted: {info.get('encrypted', False)}")

    print(f"\n📊 Collection Summary:")
    print(f"   Total files: {len(pdf_files)}")
    print(f"   Total pages: {total_pages}")

    # Save analysis to JSON
    with open("pdf_analysis.json", "w") as f:
        json.dump(collection_info, f, indent=2)

analyze_pdf_collection()
```

### Batch PDF Processing
```python
from src.core.pdf_merger import PDFMerger
import os
from pathlib import Path

def batch_process_pdf_folders():
    """Process multiple folders of PDFs."""
    merger = PDFMerger()

    # Directory containing folders of PDFs
    base_directory = "pdf_collections"

    for folder in os.listdir(base_directory):
        folder_path = Path(base_directory) / folder

        if folder_path.is_dir():
            # Find all PDFs in folder
            pdf_files = list(folder_path.glob("*.pdf"))

            if pdf_files:
                # Sort files for consistent order
                pdf_files.sort()

                # Create output filename
                output_file = f"{folder}_merged.pdf"

                print(f"\n📁 Processing folder: {folder}")
                print(f"   Found {len(pdf_files)} PDF files")

                # Merge PDFs in this folder
                success = merger.merge_with_bookmarks(
                    [str(f) for f in pdf_files],
                    output_file
                )

                if success:
                    print(f"   ✓ Created: {output_file}")
                else:
                    print(f"   ✗ Failed to create: {output_file}")

batch_process_pdf_folders()
```

## Excel Operations

### Basic Excel Merging
```python
from src.core.excel_merger import ExcelMerger

def simple_excel_merge():
    """Basic Excel file merging."""
    merger = ExcelMerger()

    excel_files = [
        "january_data.xlsx",
        "february_data.xlsx",
        "march_data.xlsx"
    ]

    # Add files to merger
    for file in excel_files:
        merger.add_file(file)

    # Merge all files
    success = merger.merge("quarterly_report.xlsx")

    if success:
        print("✓ Excel files merged successfully")
    else:
        print("✗ Excel merge failed")

simple_excel_merge()
```

### Excel Merge with Sheet Preservation
```python
from src.core.excel_merger import ExcelMerger

def excel_merge_preserve_sheets():
    """Merge Excel files while preserving sheet names."""
    merger = ExcelMerger()

    # Department budget files
    department_files = {
        "sales_budget.xlsx": "Sales",
        "marketing_budget.xlsx": "Marketing",
        "engineering_budget.xlsx": "Engineering",
        "hr_budget.xlsx": "HR"
    }

    for file_path, department in department_files.items():
        merger.add_file(file_path, sheet_prefix=department)

    success = merger.merge("company_budget.xlsx", preserve_sheet_names=True)

    if success:
        print("✓ Department budgets merged")
        print("Each department has its own sheet")

excel_merge_preserve_sheets()
```

## Automation Scripts

### Daily Report Automation
```python
from src.core.pdf_merger import PDFMerger
from datetime import datetime, timedelta
import os
import schedule
import time

def create_daily_report():
    """Automatically create daily reports from individual files."""
    merger = PDFMerger()

    # Get today's date
    today = datetime.now().strftime("%Y%m%d")

    # Look for today's report files
    report_pattern = f"report_{today}_*.pdf"
    report_files = []

    for file in os.listdir("."):
        if file.startswith(f"report_{today}_"):
            report_files.append(file)

    if report_files:
        # Sort files for consistent order
        report_files.sort()

        output_file = f"daily_summary_{today}.pdf"
        success = merger.merge_with_bookmarks(report_files, output_file)

        if success:
            print(f"✓ Created daily summary: {output_file}")
            return output_file
        else:
            print("✗ Failed to create daily summary")
    else:
        print(f"No report files found for {today}")

def create_weekly_report():
    """Create weekly summary from daily reports."""
    merger = PDFMerger()

    # Get last 7 days
    daily_reports = []
    for i in range(7):
        date = datetime.now() - timedelta(days=i)
        date_str = date.strftime("%Y%m%d")
        daily_file = f"daily_summary_{date_str}.pdf"

        if os.path.exists(daily_file):
            daily_reports.append(daily_file)

    if daily_reports:
        daily_reports.sort(reverse=True)  # Most recent first
        week_file = f"weekly_summary_{datetime.now().strftime('%Y_W%U')}.pdf"

        success = merger.merge_with_bookmarks(daily_reports, week_file)
        if success:
            print(f"✓ Created weekly summary: {week_file}")

# Schedule automation
schedule.every().day.at("18:00").do(create_daily_report)
schedule.every().sunday.at("19:00").do(create_weekly_report)

def run_scheduler():
    """Run the scheduled tasks."""
    print("🤖 Report automation started")
    print("Daily reports: 6:00 PM")
    print("Weekly reports: Sunday 7:00 PM")

    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

# Uncomment to run automation
# run_scheduler()
```

### File Organization Script
```python
from src.core.pdf_merger import PDFMerger
import os
import shutil
from pathlib import Path

def organize_and_merge_by_date():
    """Organize PDFs by date and merge by month."""
    merger = PDFMerger()

    # Source directory with mixed PDFs
    source_dir = "incoming_pdfs"
    organized_dir = "organized_pdfs"

    # Create organized directory structure
    Path(organized_dir).mkdir(exist_ok=True)

    # Process each PDF file
    for pdf_file in Path(source_dir).glob("*.pdf"):
        # Get file modification date
        file_date = datetime.fromtimestamp(pdf_file.stat().st_mtime)
        year_month = file_date.strftime("%Y-%m")

        # Create month directory
        month_dir = Path(organized_dir) / year_month
        month_dir.mkdir(exist_ok=True)

        # Copy file to month directory
        dest_file = month_dir / pdf_file.name
        shutil.copy2(pdf_file, dest_file)
        print(f"📁 {pdf_file.name} → {year_month}/")

    # Now merge each month's files
    for month_dir in Path(organized_dir).iterdir():
        if month_dir.is_dir():
            pdf_files = list(month_dir.glob("*.pdf"))

            if pdf_files:
                pdf_files.sort()  # Sort by filename
                output_file = f"monthly_archive_{month_dir.name}.pdf"

                success = merger.merge_with_bookmarks(
                    [str(f) for f in pdf_files],
                    output_file
                )

                if success:
                    print(f"✓ Created monthly archive: {output_file}")

organize_and_merge_by_date()
```

## Error Handling and Logging

### Robust Error Handling
```python
from src.core.pdf_merger import PDFMerger
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pdf_merge.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

def robust_pdf_merge_with_recovery():
    """PDF merge with comprehensive error handling."""
    merger = PDFMerger()

    input_files = [
        "file1.pdf",
        "corrupted_file.pdf",  # This might fail
        "file3.pdf"
    ]

    # Try individual file validation first
    validated_files = []
    failed_files = []

    for file_path in input_files:
        try:
            if os.path.exists(file_path):
                if merger.validate_pdf(file_path):
                    validated_files.append(file_path)
                    logging.info(f"✓ Validated: {file_path}")
                else:
                    failed_files.append(file_path)
                    logging.warning(f"⚠ Invalid PDF: {file_path}")
            else:
                failed_files.append(file_path)
                logging.error(f"✗ File not found: {file_path}")
        except Exception as e:
            failed_files.append(file_path)
            logging.error(f"✗ Error checking {file_path}: {e}")

    # Attempt merge with validated files
    if validated_files:
        try:
            success = merger.merge_with_bookmarks(
                validated_files,
                "robust_output.pdf"
            )

            if success:
                logging.info(f"✓ Successfully merged {len(validated_files)} files")
                print(f"Merge completed: {len(validated_files)} files processed")
            else:
                logging.error("✗ Merge operation failed")

        except Exception as e:
            logging.error(f"✗ Merge exception: {e}")

            # Fallback: try merging smaller batches
            logging.info("Attempting fallback: smaller batches")
            for i, file_path in enumerate(validated_files):
                try:
                    merger.merge_pdfs([file_path], f"individual_{i}.pdf")
                    logging.info(f"✓ Created individual file: individual_{i}.pdf")
                except Exception as batch_error:
                    logging.error(f"✗ Failed individual file {file_path}: {batch_error}")

    # Report results
    print(f"\nProcessing Summary:")
    print(f"✓ Successful files: {len(validated_files)}")
    print(f"✗ Failed files: {len(failed_files)}")

    if failed_files:
        print(f"\nFailed files:")
        for file_path in failed_files:
            print(f"  - {file_path}")

robust_pdf_merge_with_recovery()
```

## Integration Examples

### Web Framework Integration (Flask)
```python
from flask import Flask, request, send_file, jsonify
from src.core.pdf_merger import PDFMerger
import tempfile
import os

app = Flask(__name__)

@app.route('/merge_pdfs', methods=['POST'])
def merge_pdfs_endpoint():
    """Web API endpoint for PDF merging."""
    try:
        merger = PDFMerger()

        # Get uploaded files
        uploaded_files = request.files.getlist('pdf_files')
        temp_files = []

        # Save uploaded files temporarily
        for uploaded_file in uploaded_files:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            uploaded_file.save(temp_file.name)
            temp_files.append(temp_file.name)

        # Create output file
        output_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        output_file.close()

        # Merge PDFs
        success = merger.merge_with_bookmarks(temp_files, output_file.name)

        if success:
            # Clean up temp input files
            for temp_file in temp_files:
                os.unlink(temp_file)

            # Return merged file
            return send_file(
                output_file.name,
                as_attachment=True,
                download_name='merged_document.pdf',
                mimetype='application/pdf'
            )
        else:
            return jsonify({'error': 'PDF merge failed'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

### Command Line Tool Enhancement
```python
#!/usr/bin/env python3
"""
Enhanced CLI tool for Document Merger
"""

import argparse
import sys
from src.core.pdf_merger import PDFMerger
from src.core.excel_merger import ExcelMerger

def main():
    parser = argparse.ArgumentParser(description='Document Merger CLI Tool')
    parser.add_argument('--type', choices=['pdf', 'excel'], required=True,
                      help='Type of files to merge')
    parser.add_argument('--files', nargs='+', required=True,
                      help='Input files to merge')
    parser.add_argument('--output', required=True,
                      help='Output file path')
    parser.add_argument('--bookmarks', action='store_true',
                      help='Add bookmarks (PDF only)')
    parser.add_argument('--validate', action='store_true',
                      help='Validate files before merging')
    parser.add_argument('--verbose', '-v', action='store_true',
                      help='Verbose output')

    args = parser.parse_args()

    if args.type == 'pdf':
        merger = PDFMerger()

        # Validate files if requested
        if args.validate:
            valid_files = []
            for file_path in args.files:
                if merger.validate_pdf(file_path):
                    valid_files.append(file_path)
                    if args.verbose:
                        print(f"✓ Valid: {file_path}")
                else:
                    if args.verbose:
                        print(f"✗ Invalid: {file_path}")

            if not valid_files:
                print("Error: No valid PDF files found")
                sys.exit(1)

            files_to_merge = valid_files
        else:
            files_to_merge = args.files

        # Merge files
        if args.bookmarks:
            success = merger.merge_with_bookmarks(files_to_merge, args.output)
        else:
            success = merger.merge_pdfs(files_to_merge, args.output)

        if success:
            print(f"✓ PDF merge completed: {args.output}")
        else:
            print("✗ PDF merge failed")
            sys.exit(1)

    elif args.type == 'excel':
        merger = ExcelMerger()

        for file_path in args.files:
            merger.add_file(file_path)

        success = merger.merge(args.output)

        if success:
            print(f"✓ Excel merge completed: {args.output}")
        else:
            print("✗ Excel merge failed")
            sys.exit(1)

if __name__ == '__main__':
    main()
```

These examples demonstrate the flexibility and power of Document Merger's API. You can adapt these patterns for your specific use cases, whether you need simple merging, batch processing, automation, or integration with other systems.
