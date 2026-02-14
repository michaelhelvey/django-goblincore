from app.views.auth import LoginView, logout_view
from app.views.home import HomeView
from django.urls import path

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
]
