from django.urls import path
from app.views.home import HomeView
from app.views.widget import (
    WidgetListView,
    WidgetDetailView,
    WidgetCreateView,
    WidgetUpdateView,
    WidgetDeleteView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("widgets/", WidgetListView.as_view(), name="widget-list"),
    path("widgets/create/", WidgetCreateView.as_view(), name="widget-create"),
    path("widgets/<int:pk>/", WidgetDetailView.as_view(), name="widget-detail"),
    path("widgets/<int:pk>/update/", WidgetUpdateView.as_view(), name="widget-update"),
    path("widgets/<int:pk>/delete/", WidgetDeleteView.as_view(), name="widget-delete"),
]
