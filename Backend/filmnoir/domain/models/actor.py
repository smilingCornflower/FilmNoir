from django.db import models

from domain.constants import CHAR_FIELD_MAX_LENGTH
from domain.ports.model import AbstractModel


class Actor(AbstractModel):
    name = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    surname = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)

    def __str__(self) -> str:
        return f"{self.name} {self.surname}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'surname'], name='actor_unique_name_surname')
        ]