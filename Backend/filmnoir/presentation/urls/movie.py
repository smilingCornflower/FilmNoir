from django.urls import path
from presentation.views.movie import MovieReadView


urlpatterns = [
    path('', MovieReadView.as_view()),
]