from django.db import models

from domain.constants import CHAR_FIELD_MAX_LENGTH
from domain.ports.model import AbstractModel


class Genre(AbstractModel):
    name = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH, unique=True)

    def __str__(self) -> str:
        return self.name
