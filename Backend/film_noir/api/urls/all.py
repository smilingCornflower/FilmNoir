from django.urls import include, path


urlpatterns = [
    path('movie/', include("api.urls.movie"))
]