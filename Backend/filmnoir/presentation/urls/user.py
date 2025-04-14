from django.urls import path
from presentation.views.user import RegistrationView


urlpatterns = [
    path('register/', RegistrationView.as_view()),
]