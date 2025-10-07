#!/usr/bin/env python
"""A simple Hello World script."""


def say_hello(name="World"):
    """
    Returns a greeting message.
    
    Args:
        name (str): The name to greet. Defaults to "World".
    
    Returns:
        str: A greeting message.
    """
    return f"Hello, {name}!"


def main():
    """Main function to print Hello World."""
    message = say_hello()
    print(message)


if __name__ == "__main__":
    main()
