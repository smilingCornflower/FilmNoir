from django.contrib import admin

from serial.models import Serial


@admin.register(Serial)
class MyModelAdmin(admin.ModelAdmin[Serial]):
    autocomplete_fields = ["genres", "actors", "director"]
