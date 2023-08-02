from .models import *
import django_filters
from django import forms

class PostFilter(django_filters.FilterSet):
    author = django_filters.ModelChoiceFilter(field_name='author',
                                              label='Выбор по автору',
                                              lookup_expr='exact',
                                              queryset=Author.objects.all())
    date = django_filters.DateFilter(field_name='time_create',
                                     widget=forms.DateInput(attrs={'type': 'date'}), label='Позже даты',
                                     lookup_expr='gt')
    title = django_filters.ModelChoiceFilter(field_name='title',
                                             label='Поиск по названию',
                                             lookup_expr='icontains',
                                             queryset=Post.objects.all())


