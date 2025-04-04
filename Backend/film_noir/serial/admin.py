from django.contrib import admin

from serial.models import Serial, SerialEpisode


@admin.register(Serial)
class SerialAdmin(admin.ModelAdmin[Serial]):
    autocomplete_fields = ["genres", "actors", "director"]
    search_fields = ["title"]


@admin.register(SerialEpisode)
class SerialEpisodeAdmin(admin.ModelAdmin[SerialEpisode]):
    autocomplete_fields = ["content"]
