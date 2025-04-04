from django.urls import path

from api.views.serial import SerialView

urlpatterns = [
    path("", SerialView.as_view())
]