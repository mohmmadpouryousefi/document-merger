# Getting Started with Document Merger

This guide will help you get up and running with Document Merger quickly.

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/document-merger.git
cd document-merger
```

### Step 2: Create Virtual Environment
```bash
python -m venv document_merger_env
```

### Step 3: Activate Virtual Environment
**Windows:**
```bash
document_merger_env\Scripts\activate
```

**macOS/Linux:**
```bash
source document_merger_env/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Verify Installation
```bash
python test_installation.py
```

## Quick Start

### Using the GUI (Recommended for Beginners)
1. Run the application:
   ```bash
   python main.py
   ```
2. The GUI will open automatically
3. Click "Add Files" to select your documents
4. Choose merge type (PDF or Excel)
5. Click "Merge Files" and select output location

### Using the CLI (Advanced Users)
```bash
# Merge PDF files
python -m src.cli.cli_interface --type pdf --files file1.pdf file2.pdf --output merged.pdf

# Merge Excel files
python -m src.cli.cli_interface --type excel --files file1.xlsx file2.xlsx --output merged.xlsx
```

## What's Next?

- Check out [Usage Examples](README.md) for more detailed scenarios
- Read the [API Documentation](../api/README.md) for programmatic usage
- See [Troubleshooting](../troubleshooting.md) if you encounter issues

## Need Help?

- Check the main [README](../../README.md) for project overview
- Look at [common use cases](common_use_cases.md)
- Review [troubleshooting guide](../troubleshooting.md)
