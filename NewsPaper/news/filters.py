import django.forms
from django_filters import FilterSet, CharFilter, DateFilter, ModelChoiceFilter
from .models import Post, Author

# создаём фильтр
class PostSearch(FilterSet):
    dateCreation = DateFilter(
        lookup_expr='gte',
        widget=django.forms.DateInput(attrs={'type': 'date'})
    )
    title = CharFilter(
        field_name='title',
        lookup_expr = 'icontains',
        label = 'Название статьи'
    )
    # мы хотим чтобы нам выводило имя из списка
    author = ModelChoiceFilter(
        field_name='author',
        queryset = Author.objects.all(),
        lookup_expr=('exact'),
        label = 'Автор'
    )
    # Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться (т. е. подбираться) информация о товарах
    class Meta:
        model = Post
        fields = []
        # ('date', 'title', 'author')