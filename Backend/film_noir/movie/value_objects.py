from dataclasses import dataclass

from common.value_objects import ActorVo, ScreenContentQueryParamsVo, ContentVo, DirectorVo, VideoVo


@dataclass(frozen=True)
class MovieVo(ContentVo):
    actors: list[ActorVo]
    director: DirectorVo
    video: VideoVo | None


@dataclass(frozen=True)
class MovieQueryParamsVo(ScreenContentQueryParamsVo):
    pass
