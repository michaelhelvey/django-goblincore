import factory
from django.db import models


class Widget(models.Model):
    """
    Simple example resource exposed through the widgets API.
    """

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class WidgetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Widget

    name = factory.Sequence(lambda n: f"Widget {n}")
    description = factory.Faker("sentence")
