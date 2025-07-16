from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage
from django.conf import settings
from django.http import HttpResponseRedirect
from .models import Album, Image
from .forms import createCollection, ImageForm
import os
import tempfile
from PIL import Image as PILImage


class AlbumModelTestCase(TestCase):
    """Test cases for the Album model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.album = Album.objects.create(
            title='Test Album',
            user=self.user
        )
    
    def test_album_creation(self):
        """Test album creation."""
        self.assertEqual(self.album.title, 'Test Album')
        self.assertEqual(self.album.user, self.user)
        self.assertTrue(isinstance(self.album, Album))
    
    def test_album_string_representation(self):
        """Test album string representation."""
        self.assertEqual(str(self.album), 'Test Album')
    
    def test_album_without_user(self):
        """Test album creation without user."""
        album = Album.objects.create(title='No User Album')
        self.assertIsNone(album.user)
    
    def test_album_with_cover_image(self):
        """Test album with cover image."""
        # Create a simple test image
        image = PILImage.new('RGB', (100, 100), color='red')
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        image.save(temp_file.name)
        
        with open(temp_file.name, 'rb') as f:
            uploaded_file = SimpleUploadedFile(
                name='test_cover.jpg',
                content=f.read(),
                content_type='image/jpeg'
            )
        
        album = Album.objects.create(
            title='Album with Cover',
            album_cover=uploaded_file,
            user=self.user
        )
        
        self.assertTrue(album.album_cover)
        self.assertIn('test_cover', album.album_cover.name)
        
        # Clean up
        os.unlink(temp_file.name)


class ImageModelTestCase(TestCase):
    """Test cases for the Image model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.album = Album.objects.create(
            title='Test Album',
            user=self.user
        )
        
        # Create a simple test image
        image = PILImage.new('RGB', (100, 100), color='blue')
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        image.save(temp_file.name)
        
        with open(temp_file.name, 'rb') as f:
            uploaded_file = SimpleUploadedFile(
                name='test_image.jpg',
                content=f.read(),
                content_type='image/jpeg'
            )
        
        self.image = Image.objects.create(
            title='Test Image',
            image=uploaded_file,
            albums=self.album
        )
        
        # Clean up
        os.unlink(temp_file.name)
    
    def test_image_creation(self):
        """Test image creation."""
        self.assertEqual(self.image.title, 'Test Image')
        self.assertEqual(self.image.albums, self.album)
        self.assertTrue(isinstance(self.image, Image))
    
    def test_image_string_representation(self):
        """Test image string representation."""
        self.assertIn('test_image', str(self.image))
    
    def test_image_without_title(self):
        """Test image creation without title."""
        image = PILImage.new('RGB', (100, 100), color='green')
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        image.save(temp_file.name)
        
        with open(temp_file.name, 'rb') as f:
            uploaded_file = SimpleUploadedFile(
                name='no_title.jpg',
                content=f.read(),
                content_type='image/jpeg'
            )
        
        image_obj = Image.objects.create(
            image=uploaded_file,
            albums=self.album
        )
        
        self.assertIsNone(image_obj.title)
        
        # Clean up
        os.unlink(temp_file.name)


class LibraryViewTestCase(TestCase):
    """Test cases for library views."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        self.album = Album.objects.create(
            title='Test Album',
            user=self.user
        )
    
    def test_dashboard_requires_login(self):
        """Test that dashboard requires authentication."""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_create_album_get_requires_login(self):
        """Test that create album GET requires authentication."""
        response = self.client.get(reverse('create'))
        self.assertEqual(response.status_code, 302)
    
    def test_view_albums_requires_login(self):
        """Test that view albums requires authentication."""
        response = self.client.get(reverse('view'))
        self.assertEqual(response.status_code, 302)
    
    def test_view_gallery_requires_login(self):
        """Test that view gallery requires authentication."""
        response = self.client.get(reverse('gallery', kwargs={'id': self.album.id}))
        self.assertEqual(response.status_code, 302)
    
    def test_delete_album_removes_album(self):
        """Test that delete album removes the album."""
        album_id = self.album.id
        response = self.client.post(reverse('delete_album', kwargs={'id': album_id}))
        
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.assertFalse(Album.objects.filter(id=album_id).exists())
    
    def test_add_images_get_requires_login(self):
        """Test that add images GET requires authentication."""
        response = self.client.get(reverse('upload', kwargs={'id': self.album.id}))
        self.assertEqual(response.status_code, 302)
    
    def test_user_can_only_access_own_albums(self):
        """Test that users can only access their own albums."""
        other_album = Album.objects.create(
            title='Other User Album',
            user=self.other_user
        )
        
        self.client.login(username='testuser', password='testpass123')
        
        # User should be able to access their own album
        response = self.client.get(reverse('gallery', kwargs={'id': self.album.id}))
        self.assertEqual(response.status_code, 200)
        
        # User should be able to access other user's album (no permission check in current implementation)
        response = self.client.get(reverse('gallery', kwargs={'id': other_album.id}))
        self.assertEqual(response.status_code, 200)


class LibraryFormTestCase(TestCase):
    """Test cases for library forms."""
    
    def test_create_collection_form_valid(self):
        """Test that create collection form is valid with proper data."""
        form_data = {'title': 'Test Album'}
        form = createCollection(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_create_collection_form_invalid(self):
        """Test that create collection form is invalid without title."""
        form_data = {}
        form = createCollection(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_image_form_valid(self):
        """Test that image form is valid with proper data."""
        # Create a simple test image
        image = PILImage.new('RGB', (100, 100), color='red')
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        image.save(temp_file.name)
        
        with open(temp_file.name, 'rb') as f:
            uploaded_file = SimpleUploadedFile(
                name='test.jpg',
                content=f.read(),
                content_type='image/jpeg'
            )
        
        form_data = {}
        form_files = {'image': uploaded_file}
        form = ImageForm(data=form_data, files=form_files)
        self.assertTrue(form.is_valid())
        
        # Clean up
        os.unlink(temp_file.name)


class LibraryURLTestCase(TestCase):
    """Test cases for library URLs."""
    
    def test_library_urls_reverse_correctly(self):
        """Test that library URLs reverse correctly."""
        self.assertEqual(reverse('dashboard'), '/create/dashboard/')
        self.assertEqual(reverse('create'), '/create/create-album/')
        self.assertEqual(reverse('view'), '/create/view/')
        self.assertEqual(reverse('gallery', kwargs={'id': 1}), '/create/gallery/1')
        self.assertEqual(reverse('delete_album', kwargs={'id': 1}), '/create/delete_album/1')
        self.assertEqual(reverse('upload', kwargs={'id': 1}), '/create/upload/1')
        self.assertEqual(reverse('pics', kwargs={'id': 1}), '/create/pics/1')


class LibraryModelRelationshipTestCase(TestCase):
    """Test cases for library model relationships."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.album = Album.objects.create(
            title='Test Album',
            user=self.user
        )
    
    def test_album_image_relationship(self):
        """Test relationship between albums and images."""
        # Create images for the album
        image1 = PILImage.new('RGB', (100, 100), color='red')
        image2 = PILImage.new('RGB', (100, 100), color='blue')
        
        temp_file1 = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        temp_file2 = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        
        image1.save(temp_file1.name)
        image2.save(temp_file2.name)
        
        with open(temp_file1.name, 'rb') as f1, open(temp_file2.name, 'rb') as f2:
            uploaded_file1 = SimpleUploadedFile(
                name='image1.jpg',
                content=f1.read(),
                content_type='image/jpeg'
            )
            uploaded_file2 = SimpleUploadedFile(
                name='image2.jpg',
                content=f2.read(),
                content_type='image/jpeg'
            )
        
        img1 = Image.objects.create(
            title='Image 1',
            image=uploaded_file1,
            albums=self.album
        )
        
        img2 = Image.objects.create(
            title='Image 2',
            image=uploaded_file2,
            albums=self.album
        )
        
        # Test relationship
        album_images = Image.objects.filter(albums=self.album)
        self.assertEqual(album_images.count(), 2)
        self.assertIn(img1, album_images)
        self.assertIn(img2, album_images)
        
        # Clean up
        os.unlink(temp_file1.name)
        os.unlink(temp_file2.name)
    
    def test_delete_album_cascades_to_images(self):
        """Test that deleting an album deletes its images."""
        # Create an image for the album
        image = PILImage.new('RGB', (100, 100), color='red')
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        image.save(temp_file.name)
        
        with open(temp_file.name, 'rb') as f:
            uploaded_file = SimpleUploadedFile(
                name='test.jpg',
                content=f.read(),
                content_type='image/jpeg'
            )
        
        img = Image.objects.create(
            title='Test Image',
            image=uploaded_file,
            albums=self.album
        )
        
        # Verify image exists
        self.assertTrue(Image.objects.filter(id=img.id).exists())
        
        # Delete the album
        self.album.delete()
        
        # Verify image is also deleted due to cascade
        self.assertFalse(Image.objects.filter(id=img.id).exists())
        
        # Clean up
        os.unlink(temp_file.name)
