from django.db import models


# Create your models here.
class Movie(models.Model):
    tmdb_id = models.IntegerField() # id
    title = models.TextField() # title
    rank = models.FloatField() # vote_average
    release_date = models.DateField() # release_date
    summary = models.TextField() # overview
    poster_path = models.TextField() # poster_path
    is_adult = models.BooleanField() # adult

class Genre(models.Model):
    tmdb_id = models.IntegerField()
    name = models.TextField()

class Star(models.Model):
    tmdb_id = models.IntegerField()
    name = models.TextField()

class Ott(models.Model):
    tmdb_id = models.IntegerField() # provider_id
    name = models.TextField() # provider_name
    logo_path = models.TextField() # logo_path
    movies = models.ManyToManyField(Movie)

class Director(models.Model):
    name = models.TextField()
    movie_ids = models.JSONField(default=list)  # 각 감독이 만든 영화의 tmdb_id를 저장할 필드