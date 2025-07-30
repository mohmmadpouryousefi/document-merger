# Test Configuration for Document Merger

## Running Tests

### All Tests
```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html --cov-report=term

# Run specific test categories
python -m pytest tests/test_pdf_merger.py -v
python -m pytest tests/test_excel_merger.py -v
python -m pytest tests/test_integration.py -v
```

### Individual Test Classes
```bash
# PDF merger tests only
python -m pytest tests/test_pdf_merger.py::TestPDFMerger -v

# Excel merger tests only
python -m pytest tests/test_excel_merger.py::TestExcelMerger -v

# Integration tests only
python -m pytest tests/test_integration.py::TestDocumentMergerIntegration -v
```

### Using unittest (Alternative)
```bash
# Run all tests with unittest
python -m unittest discover tests/ -v

# Run specific test file
python -m unittest tests.test_pdf_merger -v

# Run specific test class
python -m unittest tests.test_pdf_merger.TestPDFMerger -v

# Run specific test method
python -m unittest tests.test_pdf_merger.TestPDFMerger.test_merge_pdfs_success -v
```

## Test Structure

```
tests/
├── __init__.py              # Test package initialization
├── test_pdf_merger.py       # PDF functionality tests
├── test_excel_merger.py     # Excel functionality tests  
├── test_file_merger.py      # File merger orchestrator tests
├── test_integration.py      # End-to-end integration tests
├── test_utils.py           # Test utilities and helpers
└── README.md               # This file
```

## Test Categories

### Unit Tests
- **PDF Merger**: Tests for `src.core.pdf_merger.PDFMerger`
- **Excel Merger**: Tests for `src.core.excel_merger.ExcelMerger`
- **File Merger**: Tests for `src.core.file_merger.FileMerger`

### Integration Tests
- **End-to-End Workflows**: Complete merge operations
- **File Type Detection**: Mixed file handling
- **Error Recovery**: Graceful failure handling
- **Performance**: Large file processing

### Mock Tests
- **External Dependencies**: Tests without requiring reportlab
- **Error Conditions**: Simulated failure scenarios
- **Edge Cases**: Boundary condition testing

## Test Dependencies

### Required
- `pytest` - Test framework
- `openpyxl` - Excel file handling (already in requirements)
- `PyPDF2` - PDF file handling (already in requirements)

### Optional
- `pytest-cov` - Coverage reporting
- `reportlab` - Real PDF generation for integration tests
- `pytest-xdist` - Parallel test execution

### Installation
```bash
# Install test dependencies
pip install pytest pytest-cov

# Optional dependencies for enhanced testing
pip install reportlab pytest-xdist
```

## Test Data

### Generated Test Files
Tests automatically generate temporary files:
- **PDF Files**: Minimal valid PDFs or reportlab-generated PDFs
- **Excel Files**: Multi-sheet workbooks with sample data
- **Corrupted Files**: Invalid files for error testing

### Cleanup
All test files are automatically cleaned up after each test.

## Configuration

### Environment Variables
```bash
# Skip integration tests if dependencies missing
export SKIP_INTEGRATION_TESTS=true

# Enable verbose test output
export PYTEST_VERBOSE=true

# Set custom temporary directory
export TEST_TEMP_DIR=/path/to/temp
```

### pytest.ini (Optional)
Create `pytest.ini` in project root:
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow running tests
```

## Coverage Targets

- **Overall Coverage**: > 90%
- **Core Modules**: > 95%
- **Error Handling**: > 85%
- **Integration Paths**: > 80%

## Running Specific Test Types

### Quick Tests (Fast feedback)
```bash
# Unit tests only (fast)
python -m pytest tests/test_pdf_merger.py tests/test_excel_merger.py -v

# Skip integration tests
python -m pytest tests/ -v -k "not integration"
```

### Comprehensive Tests
```bash
# All tests with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Integration tests only
python -m pytest tests/test_integration.py -v -s
```

### Continuous Integration
```bash
# CI-friendly test run
python -m pytest tests/ --cov=src --cov-report=xml --cov-fail-under=85
```

## Test Output

### Success Example
```
tests/test_pdf_merger.py::TestPDFMerger::test_merger_initialization PASSED
tests/test_pdf_merger.py::TestPDFMerger::test_validate_pdf_valid_file PASSED
tests/test_pdf_merger.py::TestPDFMerger::test_merge_pdfs_success PASSED
```

### Coverage Report
```
Name                     Stmts   Miss  Cover
--------------------------------------------
src/core/pdf_merger.py     125      8    94%
src/core/excel_merger.py   156     12    92%
src/core/file_merger.py     89      6    93%
--------------------------------------------
TOTAL                      370     26    93%
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Ensure src is in Python path
   export PYTHONPATH="${PYTHONPATH}:."
   ```

2. **Missing Dependencies**
   ```bash
   # Install optional dependencies
   pip install reportlab
   ```

3. **Permission Errors**
   ```bash
   # Ensure write permissions in temp directory
   chmod 755 /tmp
   ```

### Debug Mode
```bash
# Run with debug output
python -m pytest tests/ -v -s --tb=long

# Run single test with debugging
python -m pytest tests/test_pdf_merger.py::TestPDFMerger::test_merge_pdfs_success -v -s
```

## Contributing Tests

When adding new tests:

1. **Follow naming convention**: `test_*.py` files, `Test*` classes, `test_*` methods
2. **Include docstrings**: Describe what each test verifies
3. **Use test utilities**: Leverage `test_utils.py` for common operations
4. **Clean up resources**: Use proper setup/teardown
5. **Test edge cases**: Include error conditions and boundary cases
6. **Update documentation**: Add test descriptions to this file

### Example Test Structure
```python
class TestNewFeature(unittest.TestCase):
    """Test cases for new feature."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = TestDirectoryManager()
        self.test_dir.setup_test_directory()
    
    def tearDown(self):
        """Clean up test fixtures."""
        self.test_dir.cleanup()
    
    def test_feature_success(self):
        """Test successful feature operation."""
        # Test implementation
        pass
    
    def test_feature_error_handling(self):
        """Test feature error handling."""
        # Test error scenarios
        pass
```
