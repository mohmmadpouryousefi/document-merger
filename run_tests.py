#!/usr/bin/env python3
"""
Test runner script for Document Merger.
Provides various test execution options and reporting.
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, description=""):
    """Run a command and return success status."""
    if description:
        print(f"\n🔄 {description}")
        print("=" * 50)
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=False)
    
    if result.returncode == 0:
        print(f"✅ {description} - PASSED" if description else "✅ Command completed successfully")
    else:
        print(f"❌ {description} - FAILED" if description else "❌ Command failed")
    
    return result.returncode == 0


def install_dependencies(dev=False):
    """Install required dependencies."""
    requirements_file = "requirements-dev.txt" if dev else "requirements.txt"
    
    if not Path(requirements_file).exists():
        print(f"❌ {requirements_file} not found")
        return False
    
    return run_command([
        sys.executable, "-m", "pip", "install", "-r", requirements_file
    ], f"Installing dependencies from {requirements_file}")


def run_unit_tests(coverage=True, verbose=True):
    """Run unit tests."""
    cmd = [sys.executable, "-m", "pytest", "tests/test_pdf_merger.py", 
           "tests/test_excel_merger.py", "tests/test_file_merger.py"]
    
    if verbose:
        cmd.append("-v")
    
    if coverage:
        cmd.extend(["--cov=src", "--cov-report=term", "--cov-report=html"])
    
    return run_command(cmd, "Running unit tests")


def run_integration_tests(verbose=True):
    """Run integration tests."""
    cmd = [sys.executable, "-m", "pytest", "tests/test_integration.py"]
    
    if verbose:
        cmd.append("-v")
    
    return run_command(cmd, "Running integration tests")


def run_all_tests(coverage=True, verbose=True):
    """Run all tests."""
    cmd = [sys.executable, "-m", "pytest", "tests/"]
    
    if verbose:
        cmd.append("-v")
    
    if coverage:
        cmd.extend(["--cov=src", "--cov-report=term", "--cov-report=html", "--cov-report=xml"])
    
    return run_command(cmd, "Running all tests")


def run_specific_test(test_path, verbose=True):
    """Run a specific test file or test method."""
    cmd = [sys.executable, "-m", "pytest", test_path]
    
    if verbose:
        cmd.append("-v")
    
    return run_command(cmd, f"Running specific test: {test_path}")


def run_code_quality_checks():
    """Run code quality and linting checks."""
    checks_passed = 0
    total_checks = 0
    
    # Black formatting check
    total_checks += 1
    if run_command([sys.executable, "-m", "black", "--check", "src/", "tests/"], 
                  "Checking code formatting with Black"):
        checks_passed += 1
    
    # isort import sorting check
    total_checks += 1
    if run_command([sys.executable, "-m", "isort", "--check-only", "src/", "tests/"], 
                  "Checking import sorting with isort"):
        checks_passed += 1
    
    # flake8 linting
    total_checks += 1
    if run_command([sys.executable, "-m", "flake8", "src/", "tests/", 
                   "--max-line-length=88"], "Running flake8 linting"):
        checks_passed += 1
    
    # mypy type checking
    total_checks += 1
    if run_command([sys.executable, "-m", "mypy", "src/", "--ignore-missing-imports"], 
                  "Running mypy type checking"):
        checks_passed += 1
    
    print(f"\n📊 Code Quality Summary: {checks_passed}/{total_checks} checks passed")
    return checks_passed == total_checks


def run_security_scan():
    """Run security vulnerability scan."""
    return run_command([sys.executable, "-m", "bandit", "-r", "src/"], 
                      "Running security scan with bandit")


def generate_coverage_report():
    """Generate detailed coverage report."""
    success = run_command([sys.executable, "-m", "pytest", "tests/", 
                          "--cov=src", "--cov-report=html", "--cov-report=xml"], 
                         "Generating coverage report")
    
    if success:
        html_report = Path("htmlcov/index.html")
        if html_report.exists():
            print(f"📄 Coverage report generated: {html_report.absolute()}")
    
    return success


def validate_installation():
    """Validate that the application can be imported and basic functionality works."""
    test_script = """
import sys
import os
sys.path.insert(0, 'src')

try:
    from core.pdf_merger import PDFMerger
    from core.excel_merger import ExcelMerger
    from core.file_merger import FileMerger
    
    # Test basic initialization
    pdf_merger = PDFMerger()
    excel_merger = ExcelMerger()
    file_merger = FileMerger()
    
    print("✅ All core modules imported successfully")
    print("✅ Basic initialization works")
    
except Exception as e:
    print(f"❌ Installation validation failed: {e}")
    sys.exit(1)
"""
    
    return run_command([sys.executable, "-c", test_script], 
                      "Validating installation")


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description="Document Merger Test Runner")
    
    parser.add_argument("--install-deps", action="store_true",
                       help="Install dependencies before running tests")
    parser.add_argument("--dev-deps", action="store_true",
                       help="Install development dependencies")
    parser.add_argument("--unit", action="store_true",
                       help="Run unit tests only")
    parser.add_argument("--integration", action="store_true", 
                       help="Run integration tests only")
    parser.add_argument("--all", action="store_true", default=True,
                       help="Run all tests (default)")
    parser.add_argument("--no-coverage", action="store_true",
                       help="Skip coverage reporting")
    parser.add_argument("--quality", action="store_true",
                       help="Run code quality checks")
    parser.add_argument("--security", action="store_true",
                       help="Run security scan")
    parser.add_argument("--validate", action="store_true",
                       help="Validate installation only")
    parser.add_argument("--specific", type=str,
                       help="Run specific test (e.g., tests/test_pdf_merger.py::TestPDFMerger::test_merge_pdfs_success)")
    parser.add_argument("--quiet", action="store_true",
                       help="Reduce output verbosity")
    
    args = parser.parse_args()
    
    # Override default 'all' if specific options are chosen
    if any([args.unit, args.integration, args.quality, args.security, 
            args.validate, args.specific]):
        args.all = False
    
    verbose = not args.quiet
    use_coverage = not args.no_coverage
    
    print("🧪 Document Merger Test Runner")
    print("=" * 40)
    
    # Install dependencies if requested
    if args.install_deps:
        if not install_dependencies(dev=args.dev_deps):
            print("❌ Failed to install dependencies")
            return 1
    
    # Validate installation
    if args.validate:
        return 0 if validate_installation() else 1
    
    # Run specific test
    if args.specific:
        return 0 if run_specific_test(args.specific, verbose) else 1
    
    success_count = 0
    total_operations = 0
    
    # Run tests
    if args.unit:
        total_operations += 1
        if run_unit_tests(coverage=use_coverage, verbose=verbose):
            success_count += 1
    
    if args.integration:
        total_operations += 1
        if run_integration_tests(verbose=verbose):
            success_count += 1
    
    if args.all:
        total_operations += 1
        if run_all_tests(coverage=use_coverage, verbose=verbose):
            success_count += 1
    
    # Run quality checks
    if args.quality:
        total_operations += 1
        if run_code_quality_checks():
            success_count += 1
    
    # Run security scan
    if args.security:
        total_operations += 1
        if run_security_scan():
            success_count += 1
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📋 Test Summary: {success_count}/{total_operations} operations successful")
    
    if success_count == total_operations:
        print("🎉 All tests and checks passed!")
        return 0
    else:
        print("💥 Some tests or checks failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
