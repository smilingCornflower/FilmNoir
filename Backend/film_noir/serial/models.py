from django.db import models

from common.models.base_content import BaseContent
from common.models.base_episode import BaseEpisode
from serial.constants import SERIAL_CONTENT_TYPE, SERIAL_POSTER_PATH


class Serial(BaseContent):
    actors = models.ManyToManyField("common.actor", related_name="serials")
    director = models.ForeignKey(
        "common.director", related_name="serials", on_delete=models.PROTECT
    )

    @property
    def poster_path(self) -> str:
        return SERIAL_POSTER_PATH

    @property
    def content_type(self) -> str:
        return SERIAL_CONTENT_TYPE


class SerialEpisode(BaseEpisode):
    content = models.ForeignKey(Serial, on_delete=models.CASCADE)
