from django.urls import path

from app.views.auth import LoginView, logout_view
from app.views.home import HomeView
from app.views.widget import (
    WidgetCreateView,
    WidgetDeleteView,
    WidgetDetailView,
    WidgetListView,
    WidgetUpdateView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("widgets/", WidgetListView.as_view(), name="widget-list"),
    path("widgets/create/", WidgetCreateView.as_view(), name="widget-create"),
    path("widgets/<int:pk>/", WidgetDetailView.as_view(), name="widget-detail"),
    path("widgets/<int:pk>/update/", WidgetUpdateView.as_view(), name="widget-update"),
    path("widgets/<int:pk>/delete/", WidgetDeleteView.as_view(), name="widget-delete"),
]
