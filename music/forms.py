from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Album, Song

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields =  ['artist', 'title','is_public','album_file']

class SongForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ['title', 'song_file']