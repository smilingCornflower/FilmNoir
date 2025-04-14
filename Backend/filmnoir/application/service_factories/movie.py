from application.services.movie import MovieReadService
from infrastructure.repositories.movie import DjMovieReadRepository


class MovieServiceFactory:
    @staticmethod
    def get_read_service() -> MovieReadService:
        return MovieReadService(repository=DjMovieReadRepository())
