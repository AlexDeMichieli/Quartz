from django.test import TestCase, Client
from django.urls import reverse

class HelloWorldTestCase(TestCase):
    def test_hello_world_view(self):
        """Test that hello_world view returns correct response"""
        client = Client()
        response = client.get(reverse('hello_world'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Hello, World!")
        
    def test_hello_world_url_accessible(self):
        """Test that hello_world URL is accessible"""
        client = Client()
        response = client.get('/hello/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Hello, World!")
