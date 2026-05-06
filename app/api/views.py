from .serializers import WidgetSerializer
from app.models import Widget
from rest_framework import viewsets


class WidgetViewSet(viewsets.ModelViewSet):
    """
    Basic CRUD API for example widgets.
    """

    queryset = Widget.objects.all()
    serializer_class = WidgetSerializer
