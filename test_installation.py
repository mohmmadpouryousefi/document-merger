"""
Test script to verify the File Merger application installation and basic functionality.
"""

import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")

    try:
        from src.core.file_detector import FileTypeDetector

        detector = FileTypeDetector()
        print(f"✓ FileTypeDetector imported successfully: {type(detector).__name__}")

        from src.core.file_merger import FileMerger

        merger = FileMerger()
        print(f"✓ FileMerger imported successfully: {type(merger).__name__}")

        from src.core.pdf_merger import PDFMerger

        pdf_merger = PDFMerger()
        print(f"✓ PDFMerger imported successfully: {type(pdf_merger).__name__}")

        from src.core.excel_merger import ExcelMerger

        excel_merger = ExcelMerger()
        print(f"✓ ExcelMerger imported successfully: {type(excel_merger).__name__}")

        from src.cli.cli_interface import CLIInterface

        cli = CLIInterface()
        print(f"✓ CLIInterface imported successfully: {type(cli).__name__}")

        from src.gui.main_window import FileManagerGUI

        # Don't instantiate GUI in headless environment, just verify import
        print(f"✓ FileManagerGUI imported successfully: {FileManagerGUI.__name__}")
        print("✓ FileManagerGUI imported successfully")

        return True

    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def test_dependencies():
    """Test that all required dependencies are available."""
    print("\nTesting dependencies...")

    dependencies = [
        ("PyPDF2", "PyPDF2"),
        ("openpyxl", "openpyxl"),
        ("tkinter", "tkinter"),
        ("pathlib", "pathlib"),
    ]

    all_available = True

    for name, module in dependencies:
        try:
            __import__(module)
            print(f"✓ {name} available")
        except ImportError:
            print(f"✗ {name} not available")
            all_available = False

    return all_available


def test_basic_functionality():
    """Test basic functionality without actual files."""
    print("\nTesting basic functionality...")

    try:
        from src.core.file_detector import FileTypeDetector
        from src.core.file_merger import FileMerger

        # Test file type detector
        detector = FileTypeDetector()

        # Test with non-existent files to check error handling
        file_type, valid_files, errors = detector.validate_files([])
        if errors and "No files provided" in errors[0]:
            print("✓ Empty file list validation works")
        else:
            print("✗ Empty file list validation failed")
            return False

        # Test file merger initialization
        merger = FileMerger()
        print("✓ FileMerger initialization works")

        # Test preview with empty files
        preview = merger.preview_merge([])
        if not preview["valid"] and preview["errors"]:
            print("✓ Preview with empty files works")
        else:
            print("✗ Preview with empty files failed")
            return False

        return True

    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False


def test_file_operations():
    """Test file operations with sample data."""
    print("\nTesting file operations...")

    try:
        from src.core.file_detector import FileTypeDetector

        detector = FileTypeDetector()

        # Test file size formatting
        size_str = detector.format_file_size(1024)
        if size_str == "1.0 KB":
            print("✓ File size formatting works")
        else:
            print(f"✗ File size formatting failed: {size_str}")
            return False

        # Test supported file types
        supported_types = detector.SUPPORTED_TYPES
        if "pdf" in supported_types and "excel" in supported_types:
            print("✓ Supported file types defined correctly")
        else:
            print("✗ Supported file types not defined correctly")
            return False

        return True

    except Exception as e:
        print(f"✗ File operations test failed: {e}")
        return False


def create_sample_files():
    """Create sample files for testing (optional)."""
    print("\nCreating sample files for testing...")

    try:
        # Create a simple text file that can be used for basic testing
        sample_dir = Path("sample_files")
        sample_dir.mkdir(exist_ok=True)

        # Create a dummy text file
        sample_file = sample_dir / "test_file.txt"
        with open(sample_file, "w") as f:
            f.write("This is a sample file for testing the File Merger application.\n")
            f.write("This file can be used to test file detection and validation.\n")

        print(f"✓ Sample file created: {sample_file}")

        # Create info file
        info_file = sample_dir / "README.txt"
        with open(info_file, "w") as f:
            f.write("Sample Files Directory\n")
            f.write("=====================\n\n")
            f.write(
                "This directory contains sample files for testing the "
                "File Merger application.\n"
            )
            f.write(
                "To test with actual PDF or Excel files, add them to "
                "this directory.\n\n"
            )
            f.write("Supported formats:\n")
            f.write("- PDF: .pdf\n")
            f.write("- Excel: .xlsx, .xls, .xlsm\n")

        print(f"✓ Info file created: {info_file}")
        return True

    except Exception as e:
        print(f"✗ Sample file creation failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("           FILE MERGER - Installation Test")
    print("=" * 60)

    tests = [
        ("Imports", test_imports),
        ("Dependencies", test_dependencies),
        ("Basic Functionality", test_basic_functionality),
        ("File Operations", test_file_operations),
        ("Sample Files", create_sample_files),
    ]

    results = []

    for test_name, test_func in tests:
        print(f"\n{'-'*20} {test_name} {'-'*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 60)
    print("           TEST RESULTS")
    print("=" * 60)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {test_name}: {status}")
        if result:
            passed += 1

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! The application is ready to use.")
        print("\nYou can now run:")
        print("  GUI Mode: python main.py")
        print("  CLI Mode: python main.py --cli")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the installation.")
        if passed < total - 1:
            print("  Consider running: python setup.py")

    return passed == total


if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)
