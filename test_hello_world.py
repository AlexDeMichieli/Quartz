#!/usr/bin/env python
"""Tests for the hello_world module."""

import unittest
from hello_world import say_hello


class TestHelloWorld(unittest.TestCase):
    """Test cases for the hello_world module."""
    
    def test_say_hello_default(self):
        """Test that say_hello returns 'Hello, World!' by default."""
        result = say_hello()
        self.assertEqual(result, "Hello, World!")
    
    def test_say_hello_with_name(self):
        """Test that say_hello returns correct greeting with a name."""
        result = say_hello("Copilot")
        self.assertEqual(result, "Hello, Copilot!")
    
    def test_say_hello_with_empty_string(self):
        """Test that say_hello handles empty string."""
        result = say_hello("")
        self.assertEqual(result, "Hello, !")


if __name__ == "__main__":
    unittest.main()
