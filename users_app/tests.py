from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Profile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from PIL import Image as PILImage
import tempfile
import os


class ProfileModelTestCase(TestCase):
    """Test cases for the Profile model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
    
    def test_profile_created_automatically(self):
        """Test that profile is created automatically when user is created."""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertEqual(self.user.profile.user, self.user)
        self.assertTrue(isinstance(self.user.profile, Profile))
    
    def test_profile_string_representation(self):
        """Test profile string representation."""
        expected = f'{self.user.username} Profile'
        self.assertEqual(str(self.user.profile), expected)
    
    def test_profile_default_image(self):
        """Test that profile has default image."""
        self.assertEqual(self.user.profile.image.name, 'default.jpg')
    
    def test_profile_custom_image(self):
        """Test profile with custom image."""
        # Create a simple test image
        image = PILImage.new('RGB', (100, 100), color='red')
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        image.save(temp_file.name)
        
        with open(temp_file.name, 'rb') as f:
            uploaded_file = SimpleUploadedFile(
                name='profile.jpg',
                content=f.read(),
                content_type='image/jpeg'
            )
        
        self.user.profile.image = uploaded_file
        self.user.profile.save()
        
        self.assertIn('profile', self.user.profile.image.name)
        
        # Clean up
        os.unlink(temp_file.name)
    
    def test_profile_signal_creates_profile(self):
        """Test that creating a user creates a profile via signal."""
        new_user = User.objects.create_user(
            username='newuser',
            password='newpass123'
        )
        
        self.assertTrue(Profile.objects.filter(user=new_user).exists())
        self.assertEqual(new_user.profile.user, new_user)


class UserViewTestCase(TestCase):
    """Test cases for user views."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
    
    def test_register_get_loads(self):
        """Test that register GET loads successfully."""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
    
    def test_register_post_valid(self):
        """Test user registration with valid data."""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complex_password_123',
            'password2': 'complex_password_123'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue(User.objects.filter(username='newuser').exists())
        
        # Check that profile was created
        new_user = User.objects.get(username='newuser')
        self.assertTrue(hasattr(new_user, 'profile'))
    
    def test_register_post_invalid(self):
        """Test user registration with invalid data."""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'invalid-email',
            'password1': 'password123',
            'password2': 'different_password'
        })
        
        self.assertEqual(response.status_code, 200)  # Form errors, no redirect
        self.assertFalse(User.objects.filter(username='newuser').exists())
    
    def test_profile_requires_login(self):
        """Test that profile view requires authentication."""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_profile_get_loads(self):
        """Test that profile GET loads for authenticated user."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
    
    def test_profile_post_update_user(self):
        """Test profile update via POST."""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(reverse('profile'), {
            'username': 'updateduser',
            'email': 'updated@example.com'
        })
        
        # Should redirect back to profile
        self.assertEqual(response.status_code, 302)
        
        # Check that user was updated
        updated_user = User.objects.get(id=self.user.id)
        self.assertEqual(updated_user.username, 'updateduser')
        self.assertEqual(updated_user.email, 'updated@example.com')
    
    def test_profile_post_update_profile_image(self):
        """Test profile image update via POST."""
        self.client.login(username='testuser', password='testpass123')
        
        # Create a simple test image
        image = PILImage.new('RGB', (100, 100), color='blue')
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        image.save(temp_file.name)
        
        with open(temp_file.name, 'rb') as f:
            response = self.client.post(reverse('profile'), {
                'username': 'testuser',
                'email': 'test@example.com',
                'image': f
            })
        
        # Should redirect back to profile
        self.assertEqual(response.status_code, 302)
        
        # Check that profile image was updated
        updated_profile = Profile.objects.get(user=self.user)
        self.assertNotEqual(updated_profile.image.name, 'default.jpg')
        
        # Clean up
        os.unlink(temp_file.name)


class UserFormTestCase(TestCase):
    """Test cases for user forms."""
    
    def test_user_register_form_valid(self):
        """Test that user register form is valid with proper data."""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complex_password_123',
            'password2': 'complex_password_123'
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_user_register_form_invalid_passwords(self):
        """Test that user register form is invalid with mismatched passwords."""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'password123',
            'password2': 'different_password'
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_user_register_form_invalid_email(self):
        """Test that user register form is invalid with invalid email."""
        form_data = {
            'username': 'newuser',
            'email': 'invalid-email',
            'password1': 'password123',
            'password2': 'password123'
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_user_update_form_valid(self):
        """Test that user update form is valid with proper data."""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        form_data = {
            'username': 'updateduser',
            'email': 'updated@example.com'
        }
        form = UserUpdateForm(data=form_data, instance=user)
        self.assertTrue(form.is_valid())
    
    def test_profile_update_form_valid(self):
        """Test that profile update form is valid with proper data."""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create a simple test image
        image = PILImage.new('RGB', (100, 100), color='red')
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        image.save(temp_file.name)
        
        with open(temp_file.name, 'rb') as f:
            uploaded_file = SimpleUploadedFile(
                name='profile.jpg',
                content=f.read(),
                content_type='image/jpeg'
            )
        
        form_files = {'image': uploaded_file}
        form = ProfileUpdateForm(files=form_files, instance=user.profile)
        self.assertTrue(form.is_valid())
        
        # Clean up
        os.unlink(temp_file.name)


class UserURLTestCase(TestCase):
    """Test cases for user URLs."""
    
    def test_user_urls_reverse_correctly(self):
        """Test that user URLs reverse correctly."""
        self.assertEqual(reverse('register'), '/register/register/')
        self.assertEqual(reverse('profile'), '/register/profile/')
    
    def test_auth_urls_reverse_correctly(self):
        """Test that authentication URLs reverse correctly."""
        self.assertEqual(reverse('login'), '/login/')
        self.assertEqual(reverse('logout'), '/logout/')
        self.assertEqual(reverse('password_change'), '/password_change/')
        self.assertEqual(reverse('password_reset'), '/password_reset/')


class UserIntegrationTestCase(TestCase):
    """Integration tests for user workflows."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
    
    def test_user_registration_and_login_flow(self):
        """Test complete user registration and login flow."""
        # Register a new user
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complex_password_123',
            'password2': 'complex_password_123'
        })
        
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        
        # User should exist
        self.assertTrue(User.objects.filter(username='newuser').exists())
        
        # Profile should be created
        user = User.objects.get(username='newuser')
        self.assertTrue(hasattr(user, 'profile'))
        
        # Login with new user
        login_success = self.client.login(username='newuser', password='complex_password_123')
        self.assertTrue(login_success)
        
        # Access profile page
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
    
    def test_user_profile_update_flow(self):
        """Test complete user profile update flow."""
        # Create user
        user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        # Login
        self.client.login(username='testuser', password='testpass123')
        
        # Update profile
        response = self.client.post(reverse('profile'), {
            'username': 'updateduser',
            'email': 'updated@example.com'
        })
        
        # Should redirect
        self.assertEqual(response.status_code, 302)
        
        # User should be updated
        updated_user = User.objects.get(id=user.id)
        self.assertEqual(updated_user.username, 'updateduser')
        self.assertEqual(updated_user.email, 'updated@example.com')
        
        # Profile should still exist
        self.assertTrue(hasattr(updated_user, 'profile'))


class UserModelSignalTestCase(TestCase):
    """Test cases for user model signals."""
    
    def test_profile_created_on_user_creation(self):
        """Test that profile is created when user is created."""
        user = User.objects.create_user(
            username='signaluser',
            password='testpass123'
        )
        
        # Profile should exist
        self.assertTrue(Profile.objects.filter(user=user).exists())
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.user, user)
    
    def test_profile_saved_on_user_save(self):
        """Test that profile is saved when user is saved."""
        user = User.objects.create_user(
            username='signaluser',
            password='testpass123'
        )
        
        original_profile = user.profile
        
        # Update user
        user.email = 'updated@example.com'
        user.save()
        
        # Profile should still exist and be the same
        self.assertTrue(Profile.objects.filter(user=user).exists())
        updated_profile = Profile.objects.get(user=user)
        self.assertEqual(updated_profile.id, original_profile.id)
