from application.services.movie import MovieAppService
from domain.services.movie import MovieReadService
from infrastructure.repositories.movie import DjMovieReadRepository


class MovieServiceFactory:
    @staticmethod
    def get_read_service() -> MovieAppService:
        return MovieAppService(MovieReadService(DjMovieReadRepository()))
