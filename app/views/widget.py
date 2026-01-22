import django_filters
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
)
from django_filters.views import FilterView

from app.models import Widget


class WidgetFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains", label="Name contains")
    min_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="gte", label="Min price"
    )
    max_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="lte", label="Max price"
    )
    is_active = django_filters.BooleanFilter(label="Active only")

    class Meta:
        model = Widget
        fields = ["name", "is_active"]


class WidgetListView(LoginRequiredMixin, FilterView):
    model = Widget
    template_name = "widgets/widget_list.html"
    filterset_class = WidgetFilter
    context_object_name = "object_list"


class WidgetDetailView(LoginRequiredMixin, DetailView):
    model = Widget
    template_name = "widgets/widget_detail.html"


class WidgetCreateView(LoginRequiredMixin, CreateView):
    model = Widget
    template_name = "widgets/widget_form.html"
    fields = ["name", "description", "price", "is_active"]
    success_url = reverse_lazy("widget-list")


class WidgetUpdateView(LoginRequiredMixin, UpdateView):
    model = Widget
    template_name = "widgets/widget_form.html"
    fields = ["name", "description", "price", "is_active"]
    success_url = reverse_lazy("widget-list")


class WidgetDeleteView(LoginRequiredMixin, DeleteView):
    model = Widget
    template_name = "widgets/widget_confirm_delete.html"
    success_url = reverse_lazy("widget-list")
