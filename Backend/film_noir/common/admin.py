from django.contrib import admin
from common.models import Genre, Actor, Director


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin[Genre]):
    pass


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin[Actor]):
    pass


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin[Director]):
    pass
