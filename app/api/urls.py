from rest_framework.routers import DefaultRouter

from app.api.widgets import WidgetViewSet

router = DefaultRouter()
router.register(r"widgets", WidgetViewSet, basename="widget")

urlpatterns = router.urls
