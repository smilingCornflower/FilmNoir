from pathlib import Path

from django.db import models
from django.utils.text import slugify
from unidecode import unidecode

from domain.constants import (
    CHAR_FIELD_MAX_LENGTH,
    MOVIE_POSTER_UPLOAD_PATH,
    MOVIE_VIDEO_UPLOAD_PATH,
)
from domain.ports.model import AbstractModel


def movie_poster_upload_path(instance: "Movie", filename: str) -> str:
    ext = Path(filename).suffix
    result: Path = MOVIE_POSTER_UPLOAD_PATH / (slugify(unidecode(instance.title)) + ext)
    return str(result)


def movie_video_upload_path(instance: "Movie", filename: str) -> str:
    ext = Path(filename).suffix
    result: Path = MOVIE_VIDEO_UPLOAD_PATH / (slugify(unidecode(instance.title)) + ext)
    return str(result)


class Movie(AbstractModel):
    title = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH, unique=True)
    description = models.TextField()
    year = models.PositiveIntegerField()
    rating = models.FloatField()
    duration = models.PositiveIntegerField()
    genres = models.ManyToManyField("domain.Genre")
    actors = models.ManyToManyField("domain.Actor")
    directors = models.ManyToManyField("domain.Director")

    poster = models.FileField(upload_to=movie_poster_upload_path)
    video = models.FileField(upload_to=movie_video_upload_path, blank=True, null=True)

    def __str__(self) -> str:
        return self.title
