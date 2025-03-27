from django.contrib import admin
from movie.models import Movie


@admin.register(Movie)
class MyModelAdmin(admin.ModelAdmin[Movie]):
    search_fields = ("genres", "actors", "director")


