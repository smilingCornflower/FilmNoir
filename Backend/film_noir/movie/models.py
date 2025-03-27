from pathlib import Path

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify
from unidecode import unidecode

from common.models import Actor, Director, Genre
from movie.constants import MOVIE_POSTERS_PATH, MOVIE_VIDEOS_PATH


def _poster_upload_path(instance: "Movie", filename: str) -> str:
    ext = Path(filename).suffix
    result = MOVIE_POSTERS_PATH + slugify(unidecode(instance.title)) + ext
    return result


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    year = models.PositiveIntegerField()
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)])

    genres = models.ManyToManyField(Genre, related_name="movies")
    actors = models.ManyToManyField(Actor, related_name="movies")
    director = models.ForeignKey(
        Director, related_name="movies", on_delete=models.CASCADE
    )

    poster = models.ImageField(upload_to=_poster_upload_path)
    video = models.FileField(upload_to=MOVIE_VIDEOS_PATH, blank=True, null=True)

    def __str__(self) -> str:
        return str(self.title)
