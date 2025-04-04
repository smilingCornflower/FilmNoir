from django.db import models

from common.models.actor import Actor
from common.models.base_content import BaseContent
from common.models.base_episode import BaseEpisode
from common.models.director import Director
from serial.constants import SERIAL_CONTENT_TYPE, SERIAL_POSTER_PATH


class Serial(BaseContent):
    actors = models.ManyToManyField(Actor, related_name="serials")
    director = models.ForeignKey(Director, related_name="serials", on_delete=models.PROTECT)

    @property
    def poster_path(self) -> str:
        return SERIAL_POSTER_PATH

    @property
    def content_type(self) -> str:
        return SERIAL_CONTENT_TYPE

    def __str__(self) -> str:
        return self.title


class SerialEpisode(BaseEpisode):
    content = models.ForeignKey(Serial, related_name="episodes", on_delete=models.CASCADE)
