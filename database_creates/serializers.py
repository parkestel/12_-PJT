from rest_framework import serializers
from  .models import Genre

class GenreSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"