"""Tests for the hello_world module."""
import unittest
from unittest.mock import patch
from io import StringIO
import hello_world


class TestHelloWorld(unittest.TestCase):
    """Test cases for hello_world module."""

    def test_main_prints_hello_world(self):
        """Test that main() prints 'Hello World'."""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            hello_world.main()
            self.assertEqual(fake_output.getvalue().strip(), "Hello World")


if __name__ == "__main__":
    unittest.main()
