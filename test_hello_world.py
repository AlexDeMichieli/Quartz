#!/usr/bin/env python3
"""Test script for hello_world.py"""

import sys
import subprocess

def test_hello_world_script():
    """Test that hello_world.py outputs 'Hello World!'"""
    result = subprocess.run(
        [sys.executable, 'hello_world.py'],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Script failed with exit code {result.returncode}"
    assert result.stdout.strip() == "Hello World!", f"Expected 'Hello World!' but got '{result.stdout.strip()}'"
    print("✓ hello_world.py test passed")

def test_hello_world_function():
    """Test that the hello_world function exists and works"""
    import hello_world
    
    # Test that main function exists
    assert hasattr(hello_world, 'main'), "hello_world.main function not found"
    
    # Capture stdout
    from io import StringIO
    import sys
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    hello_world.main()
    
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    
    assert output.strip() == "Hello World!", f"Expected 'Hello World!' but got '{output.strip()}'"
    print("✓ hello_world.main() test passed")

if __name__ == "__main__":
    test_hello_world_script()
    test_hello_world_function()
    print("\nAll tests passed!")
