from common.models.base_content import BaseContent
from movie.constants import MOVIE_VIDEOS_PATH, MOVIE_POSTERS_PATH, MOVIE_CONTENT_TYPE
from typing import TypeVar
from django.db import models

T = TypeVar("T", bound="Movie")


def _video_upload_path(instance: T, filename: str) -> str:
    ext = Path(filename).suffix
    result = instance.video_path + slugify(unidecode(instance.title)) + ext
    return result


class Movie(BaseContent):
    actors = models.ManyToManyField("common.actor", related_name="movies")
    director = models.ForeignKey("common.director", related_name="movies", on_delete=models.PROTECT)
    video = models.FileField(upload_to=_video_upload_path, blank=True, null=True)

    def __str__(self) -> str:
        return str(self.title)

    @property
    def poster_path(self) -> str:
        return MOVIE_POSTERS_PATH

    @property
    def content_type(self) -> str:
        return MOVIE_CONTENT_TYPE

    @property
    def video_path(self) -> str:
        return MOVIE_VIDEOS_PATH
