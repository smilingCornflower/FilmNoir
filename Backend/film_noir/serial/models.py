from django.db import models

from content.models import BaseContent


class Serial(BaseContent):
    ...

    @property
    def poster_path(self) -> str:
        ...
