from domain.exceptions.media import MovieNotFound
from domain.models.movie import Movie
from domain.repositories.movie import MovieReadRepository
from domain.value_objects.common import Id
from domain.value_objects.filter import MovieFilter
from loguru import logger as log


class DjMovieReadRepository(MovieReadRepository):
    def get_by_id(self, id_: Id) -> Movie:
        movie: Movie | None = Movie.objects.filter(id=id_.value).first()
        if movie is None:
            raise MovieNotFound(f"Movie with id = {id_.value} not found.")
        return movie

    def get_all(self, filter_: MovieFilter) -> list[Movie]:
        if filter_.id_:
            return [self.get_by_id(id_=filter_.id_)]

        queryset = Movie.objects.all()
        if filter_.years:
            queryset = queryset.filter(year__in=[i.value for i in filter_.years])
        if filter_.min_year:
            queryset = queryset.filter(year__gte=filter_.min_year.value)
        if filter_.max_year:
            queryset = queryset.filter(year__lte=filter_.max_year.value)

        if filter_.min_rating:
            queryset = queryset.filter(rating__gte=filter_.min_rating.value)
        if filter_.max_rating:
            queryset = queryset.filter(rating__lte=filter_.max_rating.value)

        if filter_.genre_ids:
            queryset = queryset.filter(genres__id__in=[i.value for i in filter_.genre_ids])
        if filter_.actor_ids:
            queryset = queryset.filter(actors__id__in=[i.value for i in filter_.actor_ids])
        if filter_.director_ids:
            queryset = queryset.filter(directors__id__in=[i.value for i in filter_.director_ids])

        log.debug(f'SQL statement = {str(queryset.query).replace('"', '')}')
        return list(queryset.distinct())
