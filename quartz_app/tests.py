from django.test import TestCase
from django.urls import reverse
from django.http import HttpResponse

class HelloWorldTestCase(TestCase):
    def test_hello_world_view(self):
        """Test that hello world view returns correct response"""
        response = self.client.get(reverse('hello_world'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello World")
        self.assertIsInstance(response, HttpResponse)
