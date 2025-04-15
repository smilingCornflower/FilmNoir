from django.urls import path
from presentation.views.auth import RegistrationView, LoginView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path("register/", RegistrationView.as_view()),
    path("login/", LoginView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("verify/", TokenVerifyView.as_view()),
]