from django_filters import FilterSet, CharFilter, DateFilter
from .models import Post, Category
from django.forms import DateTimeInput

class PostFilter(FilterSet):
    title = CharFilter(
        field_name='title',
        label='Заголовок содержит',
        lookup_expr = 'icontains' )

    dateCreation = DateFilter(
    field_name='dateCreation',
    label='Дата создания после',
    lookup_expr = 'gt',
    widget=DateTimeInput(
        format='%d-%M-%Y',
        attrs={'type':'date'},))

    class Meta:
        model = Post
        fields = {
            'categoryType' : ['exact']
        }


