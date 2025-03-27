from rest_framework import serializers
from rest_framework.exceptions import ParseError

from common.type_aliases import GenreT, YearT
from common.value_objects import ActorVo, DirectorVo
from movie.value_objects import MovieQueryParamsVo, MovieVo
from film_noir.settings import logger

class MovieQueryParamsSerializer:
    def __init__(self, data):
        self._data = data

    def _get_vo(self) -> MovieQueryParamsVo:
        years: list[YearT] = [int(i) for i in self._data.getlist("years", [])]
        genres: list[GenreT] = [str(i) for i in self._data.getlist("genres", [])]
        actors: list[ActorVo] = []

        for i in self._data.getlist("actors", []):
            name, surname = i.split()
            actors.append(ActorVo(name=name, surname=surname))
        directors: list[DirectorVo] = []
        for i in self._data.getlist("directors", []):
            name, surname = i.split()
            directors.append(DirectorVo(name=name, surname=surname))

        return MovieQueryParamsVo(
            years=years, genres=genres, actors=actors, directors=directors
        )

    def get_vo(self):
        """
        :raise ParseError:
        """
        try:
            return self._get_vo()
        except ValueError as e:
            logger.error(e)
            raise ParseError("Incorrect request")


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()
    year = serializers.IntegerField()
    rating = serializers.FloatField()

    genres = serializers.SerializerMethodField()
    actors = serializers.SerializerMethodField()
    director = serializers.SerializerMethodField()

    def get_genres(self, obj: MovieVo) -> list[str]:
        return [genre.name for genre in obj.genres.all()]

    def get_actors(self, obj: MovieVo) -> list[str]:
        return [actor.name + " " + actor.surname for actor in obj.actors.all()]

    def get_director(self, obj: MovieVo) -> str:
        return obj.director.name + " " + obj.director.surname
