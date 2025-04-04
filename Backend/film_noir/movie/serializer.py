from rest_framework import serializers

from common.serializer import BaseContentSerializer
from movie.models import Movie


class MovieSerializer(BaseContentSerializer):
    actors = serializers.SerializerMethodField()
    director = serializers.SerializerMethodField()
    video = serializers.CharField()

    @staticmethod
    def get_actors(obj: Movie) -> list[str]:
        return [actor.name + " " + actor.surname for actor in obj.actors.all()]

    @staticmethod
    def get_director(obj: Movie) -> str:
        return obj.director.name + " " + obj.director.surname
