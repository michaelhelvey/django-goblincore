from .views import WidgetViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("widgets", WidgetViewSet, basename="widget")

urlpatterns = router.urls
