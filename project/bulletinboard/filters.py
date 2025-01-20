from django_filters import FilterSet, CharFilter, ModelChoiceFilter, DateFilter
from .models import Post, Category, Author
from django import forms


class PostFilter(FilterSet):
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Заголовок',
    )

    category = ModelChoiceFilter(
        field_name='category',
        queryset=Category.objects.all(),
        label='Категория',
    )

    author = ModelChoiceFilter(
        field_name='author',
        queryset=Author.objects.all(),
        label='Автор',
    )

    date_time = DateFilter(
        field_name='post_time_in',
        lookup_expr='date__gte',
        label='Дата публикации после',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )

    class Meta:
        model = Post
        fields = ['title', 'category', 'date_time']
