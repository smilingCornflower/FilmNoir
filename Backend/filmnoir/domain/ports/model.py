from django.db import models
from abc import abstractmethod
from abc import abstractmethod

from django.db import models


class AbstractModel(models.Model):
    class Meta:
        abstract = True

    @abstractmethod
    def __str__(self) -> str:
        pass
