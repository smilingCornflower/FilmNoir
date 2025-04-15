from django.urls import path, include

urlpatterns = [
    path("movies/", include("presentation.urls.movie")),
    path("auth/", include("presentation.urls.auth")),
]