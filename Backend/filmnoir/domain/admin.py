from typing import TYPE_CHECKING

from django.contrib import admin

from domain.models.actor import Actor
from domain.models.director import Director
from domain.models.genre import Genre
from domain.models.movie import Movie

if TYPE_CHECKING:
    from django_stubs_ext import monkeypatch

    monkeypatch()
    GenreModelAdmin = admin.ModelAdmin[Genre]
    ActorModelAdmin = admin.ModelAdmin[Actor]
    DirectorModelAdmin = admin.ModelAdmin[Director]
    MovieModelAdmin = admin.ModelAdmin[Movie]
else:
    GenreModelAdmin = admin.ModelAdmin
    ActorModelAdmin = admin.ModelAdmin
    DirectorModelAdmin = admin.ModelAdmin
    MovieModelAdmin = admin.ModelAdmin


@admin.register(Genre)
class GenreAdmin(GenreModelAdmin):
    search_fields = ["name"]
    sortable_by = ["name"]


@admin.register(Actor)
class ActorAdmin(ActorModelAdmin):
    list_display = ["name", "surname"]
    search_fields = ["name", "surname"]
    sortable_by = ["name", "surname"]


@admin.register(Director)
class DirectorAdmin(DirectorModelAdmin):
    list_display = ["name", "surname"]
    search_fields = ["name", "surname"]
    sortable_by = ["name", "surname"]


@admin.register(Movie)
class MovieAdmin(MovieModelAdmin):
    list_display = ["title", "year"]
    sortable_by = ["id", "title", "year"]
    search_fields = ["title"]
    autocomplete_fields = ["genres", "actors", "directors"]
