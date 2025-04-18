from domain.models.movie import Movie
from domain.repositories.movie import MovieReadRepository
from domain.value_objects.common import Id
from domain.value_objects.filter import MovieFilter


class MovieReadService:
    def __init__(self, repository: MovieReadRepository):
        self.repository = repository

    def get_by_id(self, id_: Id) -> Movie:
        """:raises MovieNotFound:"""
        return self.repository.get_by_id(id_)

    def get_all(self, filter_: MovieFilter) -> list[Movie]:
        return self.repository.get_all(filter_)
