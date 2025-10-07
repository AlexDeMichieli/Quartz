from django.test import TestCase
from django.urls import reverse

# Create your tests here.

class HelloWorldViewTest(TestCase):
    """Test the Hello World view."""
    
    def test_hello_world_view(self):
        """Test that the hello world view returns 'Hello World!'"""
        response = self.client.get(reverse('hello_world'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "Hello World!")
