from django.db import models
from typing import TYPE_CHECKING
from pathlib import Path
from django.utils.text import slugify
from unidecode import unidecode
from common.constants import EPISODES_PATH
from common.models.base_content import BaseContent


def _episode_upload_path(instance: "BaseEpisode", filename: str) -> str:
    ext = Path(filename).suffix
    content_title = slugify(unidecode(instance.content.title))
    content_type = instance.content.content_type
    result = f"{EPISODES_PATH}{content_type}/{content_title}/{instance.episode_number}{ext}"
    return result


class BaseEpisode(models.Model):
    content = models.ForeignKey(BaseContent, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    episode_number = models.PositiveIntegerField()
    video = models.FileField(upload_to=_episode_upload_path)

    def __str__(self) -> str:
        return f"{self.content.title} — Episode {self.episode_number}"

    class Meta:
        abstract = True
