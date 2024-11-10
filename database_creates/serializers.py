from rest_framework import serializers
from .models import Genre, MovieLanguage, Stars


class GenreSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class MovieLanguageSerialzier(serializers.ModelSerializer):
    class Meta:
        model = MovieLanguage
        fields = "__all__"


class StarsSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Stars
        fields = "__all__"
