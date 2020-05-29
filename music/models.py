from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

def albumUploadLocation(instance, filename):
    return 'albums/{user}/{filename}'.format(user=instance.user.username, filename=filename)

def songUploadLocation(instance, filename):
    return 'songs/{user}/{filename}'.format(user=instance.album.user.username, filename=filename)

class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    artist = models.CharField(max_length=50)
    album_file = models.ImageField(upload_to=albumUploadLocation, null=True)
    is_public = models.BooleanField(default='False')

    def  __str__(self):
        return self.title+' - '+self.artist

    def get_absolute_url(self):
        return reverse("music-detail", kwargs={"id": self.pk})

class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    song_file = models.FileField(upload_to=songUploadLocation, null=True)
    is_favorite = models.BooleanField(default='False')
    is_public = models.BooleanField(default='False')

    def __str__(self):
        return self.title

    
