from abc import ABC, abstractmethod

from domain.models.movie import Movie
from domain.ports.repository import AbstractRepository
from domain.value_objects.common import Id
from domain.value_objects.filter import MovieFilter


class MovieReadRepository(AbstractRepository[Movie, MovieFilter], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> Movie:
        """:raises MovieNotFound:"""
        pass

    @abstractmethod
    def get_all(self, filter_: MovieFilter) -> list[Movie]:
        pass
