from django.db import models


# Create your models here.
class MovieLanguage:
    tmdb_id = models.IntegerField()
    name = models.TextField()


class Stars:
    tmdb_id = models.IntegerField()
    name = models.TextField()


class Genre:
    tmdb_id = models.IntegerField()
    name = models.TextField()


class Ott:
    tmdb_id = models.IntegerField()
    name = models.TextField()


class Director:
    name = models.TextField()


class Education:
    tmdb_id = models.IntegerField()


class Movie(models.Model):
    tmdb_id = models.IntegerField()
    title = models.TextField()
    summary = models.TextField()
    is_adult = models.BooleanField()
    poster_url = models.TextField()
    rank = models.FloatField()
    runtime = models.IntegerField()
    difficulty = models.FloatField(default=0)
    release_date = models.DateField()
    languages = models.ManyToManyField(Language, related_name="used_languages")
    starrings = models.ManyToManyField(Stars, related_name="stared_movie")
    genres = models.ManyToManyField(Genre, related_name="included_movies")
    otts = models.ManyToManyField(Ott, related_name="provide_movies")
    directors = models.ManyToManyField(Director, related_name="directed_movies")
    is_for_education = models.BooleanField(default=False)
