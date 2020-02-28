from django import forms
from .models import Album, Image

class createCollection(forms.ModelForm):

    class Meta:
        model = Album
        fields = ('title', 'album_cover')


class ImageForm(forms.ModelForm):

    image = forms.ImageField(label='Image')    
    class Meta:
        model = Image
        fields = ('image', )