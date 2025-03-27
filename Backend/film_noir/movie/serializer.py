from typing import Iterable

from rest_framework import serializers

from movie.models import Movie


class MovieSerializer(serializers.Serializer[Movie | Iterable[Movie]]):
    id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()
    year = serializers.IntegerField()
    rating = serializers.FloatField()

    genres = serializers.SerializerMethodField()
    actors = serializers.SerializerMethodField()
    director = serializers.SerializerMethodField()

    @staticmethod
    def get_genres(obj: Movie) -> list[str]:
        return [genre.name for genre in obj.genres.all()]

    @staticmethod
    def get_actors(obj: Movie) -> list[str]:
        return [actor.name + " " + actor.surname for actor in obj.actors.all()]

    @staticmethod
    def get_director(obj: Movie) -> str:
        return obj.director.name + " " + obj.director.surname
