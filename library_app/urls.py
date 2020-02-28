from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-album/', views.createAlbum, name="create"),
    path('view/', views.viewAlbums, name="view"),
    path('gallery/<int:id>', views.viewGallery, name ='gallery' ),
    path('delete_album/<int:id>', views.delete_album, name = 'delete_album'),
    path('delete_images/<int:id>', views.delete_images, name = 'delete_images'),
    path('upload/<int:id>', views.addImages, name = 'upload'),
    path('pics/<int:id>', views.viewPicturesByAlbum, name="pics"),
    
]