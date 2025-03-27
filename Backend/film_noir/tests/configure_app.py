import os

import django


def configure() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "film_noir.settings")
    django.setup()