from django.contrib import admin
from common.models import Genre, Actor, Director


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin[Genre]):
    search_fields = ["name"]


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin[Actor]):
    search_fields = ["name", "surname"]


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin[Director]):
    search_fields = ["name", "surname"]
