"""
Simple test to verify test infrastructure works.
"""

import unittest
import tempfile
import os
import sys
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestInfrastructure(unittest.TestCase):
    """Test that our testing infrastructure works correctly."""
    
    def test_python_imports(self):
        """Test that Python modules can be imported."""
        import tempfile
        import os
        import sys
        self.assertTrue(True)
    
    def test_file_operations(self):
        """Test basic file operations work."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            test_content = "Hello, test!"
            f.write(test_content)
            f.flush()
            temp_name = f.name
        
        # Read it back after file is closed
        with open(temp_name, 'r') as read_f:
            content = read_f.read()
            self.assertEqual(content, test_content)
        
        # Clean up
        os.unlink(temp_name)
    
    def test_pathlib_operations(self):
        """Test pathlib functionality."""
        temp_dir = Path(tempfile.mkdtemp())
        test_file = temp_dir / "test.txt"
        
        test_file.write_text("Test content")
        self.assertTrue(test_file.exists())
        
        content = test_file.read_text()
        self.assertEqual(content, "Test content")
        
        # Clean up
        test_file.unlink()
        temp_dir.rmdir()
    
    def test_src_path_available(self):
        """Test that src directory is accessible."""
        src_path = Path(__file__).parent.parent / "src"
        self.assertTrue(src_path.exists(), f"src directory should exist at {src_path}")
        
        # Check for core modules
        core_path = src_path / "core"
        self.assertTrue(core_path.exists(), f"core directory should exist at {core_path}")


if __name__ == '__main__':
    unittest.main()
