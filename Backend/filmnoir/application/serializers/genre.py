from rest_framework import serializers
from domain.models.genre import Genre


class GenreSerializer(serializers.ModelSerializer[Genre]):
    class Meta:
        model = Genre
        fields = "__all__"
