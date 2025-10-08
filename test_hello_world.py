#!/usr/bin/env python3
"""
Tests for the hello_world.py script.
"""

import unittest
from io import StringIO
import sys
import hello_world


class TestHelloWorld(unittest.TestCase):
    """Test cases for hello_world module."""
    
    def test_main_prints_hello_world(self):
        """Test that main() prints 'Hello, World!'"""
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        # Call the main function
        hello_world.main()
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        # Check output
        self.assertEqual(captured_output.getvalue().strip(), "Hello, World!")


if __name__ == "__main__":
    unittest.main()
