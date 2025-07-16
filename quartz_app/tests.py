from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied


class QuartzAppTestCase(TestCase):
    """Test cases for the main Quartz application."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
    
    def test_index_view_loads(self):
        """Test that the index page loads successfully."""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
    
    def test_index_url_resolves(self):
        """Test that the index URL resolves to the correct view."""
        url = reverse('index')
        self.assertEqual(url, '/')
    
    def test_index_uses_correct_template(self):
        """Test that index view uses the correct template."""
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'navigation/index.html')


class URLTests(TestCase):
    """Test URL routing for quartz_app."""
    
    def test_index_url_reverses_correctly(self):
        """Test that the index URL name reverses correctly."""
        url = reverse('index')
        self.assertEqual(url, '/')
    
    def test_index_url_accessible(self):
        """Test that the index URL is accessible."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
