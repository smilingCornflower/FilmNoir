from django.urls import path

from movie.views import MovieView

urlpatterns = [
    path("", MovieView.as_view())
]