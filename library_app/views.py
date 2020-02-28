from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import createCollection
import boto3
# from decouple import config

from django.conf import settings
from .models import Album
from .models import Image


@login_required
def dashboard(request):
    return render(request, 'collections/dashboard.html' )

##creates the album
@login_required
def createAlbum(request):

    if request.method == 'POST':
        title = request.POST.get('title')
        album_cover = request.FILES.get('album_cover')
        user = request.user
        new_album = Album.objects.create(
            title = title,
            album_cover = album_cover,
            user = user
        )
        albums = Album.objects.get(id = new_album.id)

        context = {
            "albums" : albums,
        }
        return render(request, 'collections/view_images.html', context )
    else:
        return render(request, 'collections/create_album.html' )
  

##deletes the album and images associated
def delete_album(request, id):
    albums = Album.objects.get(id = id)
    images = Image.objects.filter( albums = albums.id )
    s3 = boto3.resource('s3')
    for image in images:
        s3.Object('django-image-library', image.image.name).delete()
        print(image.image.name)
    s3.Object('django-image-library', albums.album_cover.name).delete()
    albums.delete()
    # # bucket = s3.Bucket('django-image-library')
    # # for x in bucket.objects.all():
    # #     print(x)
    return redirect('view')

@login_required
def delete_images(request, id):
    image = Image.objects.get(id = id)
    albums = Album.objects.get(id = image.albums.id)
    s3 = boto3.resource('s3')
    # bucket = s3.Bucket('django-image-library')
    # for x in bucket.objects.all():
    #     print(x)
    s3.Object('django-image-library', image.image.name).delete()
    image.delete()

    images = Image.objects.filter( albums = albums.id )
    context = {
        'images' : images,
        'albums': albums,
            }

    return render(request, 'collections/view_images.html', context )

##overview on the albums
@login_required
def viewAlbums(request):

    user = request.user
    albums = Album.objects.filter(user = request.user)
    context = {
            'albums' : albums,
            'user': user,
        }
    return render(request, 'collections/view_albums.html', context )

#view pictures inside albums
@login_required
def viewPicturesByAlbum (request, id): 
    
    albums = Album.objects.get(id = id)
    images = Image.objects.filter( albums = albums.id )

    context = {

            'images' : images,
            'albums': albums,
        }

    return render(request, 'collections/view_images.html', context )

@login_required
def viewGallery(request, id):

    albums = Album.objects.get(id = id)
    images = Image.objects.filter( albums = albums.id )

    context = {

            'images' : images,
            'albums': albums,
        }

    return render(request, 'collections/fluid-gallery.html', context )



@login_required
def addImages(request, id):

    if request.method == 'POST':
        albums = Album.objects.get(id = id)
        for afile in request.FILES.getlist('image_file'):
      
            Image.objects.create(
                image = afile,
                albums = albums
            )
            
        images = Image.objects.filter( albums = albums.id )
        context = {

            'images' : images,
            'albums': albums,
            }

        return render(request, 'collections/view_images.html', context )

    else:
        albums = Album.objects.get(id = id)
        context = {
            'albums': albums,
        }

        return render(request, 'collections/add_images.html', context) 
    