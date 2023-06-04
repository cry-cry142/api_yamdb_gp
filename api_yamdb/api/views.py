from rest_framework import filters, mixins, viewsets
from django_filters.rest_framework import (DjangoFilterBackend, CharFilter,
                                           FilterSet)
from django.db.models import Avg

from .serializers import (CategorySerializer, GenreSerializer,
                          TitleSerializer, TitleReadOnlySerializer)
from reviews.models import Genre, Title, Category


class CreateListDestroyViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    pass


class TitleFilterSet(FilterSet):
    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name='genre__slug')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilterSet

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleReadOnlySerializer
        return TitleSerializer
