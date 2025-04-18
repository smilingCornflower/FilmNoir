from application.dto.movie import MovieDto
from domain.models.movie import Movie


def convert_movie_to_dto(movie: Movie) -> MovieDto:
    return MovieDto(
        id=movie.id,
        title=movie.title,
        description=movie.description,
        year=movie.year,
        rating=movie.rating,
        duration=movie.duration,
        genres=[{"id": genre.id, "name": genre.name} for genre in movie.genres.all()],
        actors=[{"id": actor.id, "name": actor.name, "surname": actor.surname} for actor in movie.actors.all()],
        directors=[{"id": director.id, "name": director.name, "surname": director.surname} for director in movie.directors.all()],
        poster_url=movie.poster.url,
        video_url=movie.video.url if movie.video else None,
    )


def convert_movies_to_dto(movies: list[Movie]) -> list[MovieDto]:
    return [convert_movie_to_dto(movie) for movie in movies]
