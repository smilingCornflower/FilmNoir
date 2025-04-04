from dataclasses import dataclass

from common.type_aliases import DescriptionT, GenreT, IdT, RatingT, TitleT, YearT


@dataclass(frozen=True)
class GenreVo:
    id: IdT
    name: str


@dataclass(frozen=True)
class ActorVo:
    name: str
    surname: str


@dataclass(frozen=True)
class DirectorVo:
    name: str
    surname: str


@dataclass(frozen=True)
class PosterVo:
    path: str


@dataclass(frozen=True)
class VideoVo:
    path: str


@dataclass(frozen=True)
class ContentVo:
    id: IdT
    title: TitleT
    description: DescriptionT
    year: YearT
    rating: RatingT
    genres: list[GenreVo]
    poster: PosterVo


@dataclass(frozen=True)
class ContentQueryParamsVo:
    years: list[YearT]
    genres: list[GenreT]


@dataclass(frozen=True)
class EpisodeVo:
    content_id: IdT
    episode_number: int
    episode_path: str


@dataclass(frozen=True)
class ScreenContentQueryParamsVo(ContentQueryParamsVo):
    actors: list[ActorVo]
    directors: list[DirectorVo]