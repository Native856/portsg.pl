import django_filters
from .models import *
from django_filters import CharFilter, DateFilter
from django import forms
from django.forms import widgets
from django.forms.widgets import TextInput, Textarea


class BookFilter(django_filters.FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains')
    author = CharFilter(field_name='author', lookup_expr='icontains')

    pub_date = django_filters.DateTimeFromToRangeFilter(
        lookup_expr=('icontains'),
        widget=django_filters.widgets.RangeWidget(
            attrs={'type': 'date', 'class': 'form-control'}
        )
    )

    class Meta:
        model = BookModels
        fields = ('title', 'pub_date', 'pub_lang',)

# Widget dla daty z czasem
    # pub_date = django_filters.DateTimeFromToRangeFilter(
    #     lookup_expr=('icontains'),
    #     widget=django_filters.widgets.RangeWidget(
    #         attrs={'type':'datetime-local'}
    #     )
    # )
