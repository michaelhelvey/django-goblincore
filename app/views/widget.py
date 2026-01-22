import django_filters
from django import forms
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
    name = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
        label="Name",
        widget=forms.TextInput(attrs={"class": "input input-bordered w-full"}),
    )
    min_price = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="gte",
        label="Min Price",
        widget=forms.NumberInput(attrs={"class": "input input-bordered w-full"}),
    )
    max_price = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="lte",
        label="Max Price",
        widget=forms.NumberInput(attrs={"class": "input input-bordered w-full"}),
    )
    is_active = django_filters.ChoiceFilter(
        field_name="is_active",
        label="Status",
        empty_label="All",
        choices=[
            (True, "Active"),
            (False, "Inactive"),
        ],
        widget=forms.Select(attrs={"class": "select select-bordered w-full"}),
    )

    class Meta:
        model = Widget
        fields = []


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
