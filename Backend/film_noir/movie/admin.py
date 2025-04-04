from django.contrib import admin

from movie.models import Movie


@admin.register(Movie)
class MyModelAdmin(admin.ModelAdmin[Movie]):
    autocomplete_fields = ['genres', 'actors', 'director']