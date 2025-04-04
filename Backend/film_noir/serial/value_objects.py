from dataclasses import dataclass

from common.value_objects import ActorVo, ScreenContentQueryParamsVo, ContentVo, DirectorVo, VideoVo, EpisodeVo


@dataclass(frozen=True)
class SerialVo(ContentVo):
    actors: list[ActorVo]
    director: DirectorVo
    episodes: list[EpisodeVo]


@dataclass(frozen=True)
class SerialQueryParamsVo(ScreenContentQueryParamsVo):
    pass

