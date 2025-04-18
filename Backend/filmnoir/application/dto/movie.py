from dataclasses import dataclass


@dataclass(frozen=True)
class MovieDto:
    id: int
    title: str
    description: str
    year: int
    rating: float
    duration: int
    genres: list[dict[str, int | str]]
    actors: list[dict[str, int | str]]
    directors: list[dict[str, int | str]]
    poster_url: str
    video_url: str | None
