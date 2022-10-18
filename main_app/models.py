from django.db import models
import time
from django.contrib.auth.models import User


class Champion(models.Model):

    champion = models.CharField(max_length=100)
    image = models.CharField(max_length=500)
    bio = models.TextField(max_length=500)
    favorite_champion = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['champion']


class Song(models.Model):

    title = models.CharField(max_length=150)
    length = models.IntegerField(default=0)
    champion = models.ForeignKey(
        Champion, on_delete=models.CASCADE, related_name="songs")

    def __str__(self):
        return self.title

    def get_length(self):
        return time.strftime("%-M:%S", time.gmtime(self.length))


class Playlist(models.Model):

    title = models.CharField(max_length=150)
    songs = models.ManyToManyField(Song)

    def __str__(self):
        return self.title
