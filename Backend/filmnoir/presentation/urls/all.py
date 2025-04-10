from django.urls import path, include

urlpatterns = [
    path("movies/", include("presentation.urls.movie")),
]