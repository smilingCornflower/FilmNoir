from django.db import models


class Director(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.name} {self.surname}"
