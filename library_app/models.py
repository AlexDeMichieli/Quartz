from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
import PIL
from PIL import Image

class Album(models.Model):
    title = models.CharField(max_length=60)
    album_cover = models.ImageField(upload_to="images/",  blank=True, null=True, )
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True, blank=True)

    # public = models.BooleanField(default=False)
    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     img = PIL.Image.open(self.album_cover.path)
    #     rgb_im = img.convert('RGB')
    #     if rgb_im.height > 300 or rgb_im.width > 300:
    #         output_size = (400,400)
    #         rgb_im.thumbnail(output_size)
    #         rgb_im.save(self.album_cover.path)


class Image(models.Model):
    title = models.CharField(max_length=60, blank=True, null=True)
    image = models.ImageField(upload_to="images/" )
    albums = models.ForeignKey(Album, on_delete = models.CASCADE, blank=True)

    def __str__(self):
        return self.image.name
    
    # def delete(self, *args, **kwargs):
    #     self.image.delete()
    #     super().delete(*args, **kwargs)


    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     img = PIL.Image.open(self.image.path)
    #     rgb_im = img.convert('RGB')
    #     output_size = (800,800)
    #     rgb_im.thumbnail(output_size)
    #     rgb_im.save(self.image.path)


