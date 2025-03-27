from dataclasses import dataclass
from common.type_aliases import IdT


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
