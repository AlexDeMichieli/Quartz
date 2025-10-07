"""
Test file for hello_world.py
"""
import unittest
from unittest.mock import patch
from io import StringIO
import hello_world


class TestHelloWorld(unittest.TestCase):
    """Test cases for the hello_world module."""

    def test_main_prints_hello_world(self):
        """Test that main() prints 'Hello, World!' to stdout."""
        # Capture stdout using mock.patch for proper cleanup
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            # Call the main function
            hello_world.main()
            
            # Assert the output
            self.assertEqual(mock_stdout.getvalue().strip(), "Hello, World!")


if __name__ == "__main__":
    unittest.main()
