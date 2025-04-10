from rest_framework import serializers

from application.serializers.actor import ActorSerializer
from application.serializers.director import DirectorSerializer
from application.serializers.genre import GenreSerializer
from domain.models.movie import Movie


class MovieSerializer(serializers.ModelSerializer[Movie]):
    genres = GenreSerializer(many=True)
    actors = ActorSerializer(many=True)
    directors = DirectorSerializer(many=True)

    class Meta:
        model = Movie
        fields = "__all__"
