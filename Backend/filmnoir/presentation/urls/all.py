from django.urls import path, include

urlpatterns = [
    path("movies/", include("presentation.urls.movie")),
    path("users/", include("presentation.urls.user")),
]