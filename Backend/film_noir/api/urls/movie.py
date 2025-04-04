from django.urls import path

from api.views.movie import MovieView

urlpatterns = [
    path("", MovieView.as_view())
]