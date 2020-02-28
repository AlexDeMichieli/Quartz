from django.db import models
from django.contrib.auth.models import User
from PIL import Image


##the receiver automatically assigns a profile picture to new registered users. Post_save works with that
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     img = Image.open(self.image.path)
    #     rgb_im = img.convert('RGB')
    #     if rgb_im.height > 300 or rgb_im.width > 300:
    #         output_size = (400,400)
    #         rgb_im.thumbnail(output_size)
    #         rgb_im.save(self.image.path)


##these functions are combined with the receiver 
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()