from abc import abstractmethod
from pathlib import Path
from typing import TypeVar

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from common.models.genre import Genre
from django.utils.text import slugify
from unidecode import unidecode


def _poster_upload_path(instance: "BaseContent", filename: str) -> str:
    ext = Path(filename).suffix
    result = instance.poster_path + slugify(unidecode(instance.title)) + ext
    return result


class BaseContent(models.Model):
    @property
    @abstractmethod
    def poster_path(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def content_type(self) -> str:
        raise NotImplementedError

    title = models.CharField(max_length=255)
    description = models.TextField()
    year = models.PositiveIntegerField()
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)])

    genres = models.ManyToManyField(Genre)
    poster = models.ImageField(upload_to=_poster_upload_path)

    class Meta:
        abstract = True
