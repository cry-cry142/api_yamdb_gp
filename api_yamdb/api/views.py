from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django_filters.rest_framework import (
    DjangoFilterBackend, CharFilter, FilterSet
)
from django.shortcuts import get_object_or_404

from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.pagination import PageNumberPagination

from reviews.models import User, Genre, Title, Category, Review
from .permissions import IsAdminOrReadOnly, IsResponsibleUserOrReadOnly
from .serializers import (
    SignUpSerializer, RecieveTokenSerializer, UserSerializer,
    CategorySerializer, GenreSerializer, TitleSerializer,
    TitleReadOnlySerializer, CategorySerializer, GenreSerializer
)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def sign_up(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.create(**serializer.validated_data)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Yamdb registration success.',
            message=(
                f'Регистрация пользователя {user.username} прошла успешно.\n'
                f'Код подтверждения: {confirmation_code}'
            ),
            from_email='Yamdb@yandex.ru',
            recipient_list=[user.email],
            fail_silently=False
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def recieve_token(request):
    serializer = RecieveTokenSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        return Response(
            {'confirmation_code': 'Некорректный код подтверждения.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    def get_permissions(self):
        if self.kwargs.get('slug') == 'me':
            return (permissions.IsAuthenticated(),)
        return (permissions.IsAdminUser(),)

    def get_object(self):
        if self.kwargs.get('slug') == 'me':
            self.kwargs['pk'] = self.request.user.pk
        return super(UserViewSet, self).get_object()

    def update(self, request, slug):
        if self.kwargs.get('slug') == 'me' and self.request.data.get('role'):
            return Response(
                {'role': 'Запрещено устанавливать себе права доступа.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().update(request)


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
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilterSet

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleReadOnlySerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    http_method_names = [
        'get', 'post', 'patch', 'delete', 'head', 'options', 'trace'
    ]
    serializer_class = ReviewSerializer
    permission_classes = (IsResponsibleUserOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        queryset = title.reviews.select_related('author').all()
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(
            author=self.request.user,
            title=title
        )


class CommentViewSet(viewsets.ModelViewSet):
    http_method_names = [
        'get', 'post', 'patch', 'delete', 'head', 'options', 'trace'
    ]
    serializer_class = CommentSerializer
    permission_classes = (IsResponsibleUserOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        queryset = review.comments.select_related('author').all()
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(
            author=self.request.user,
            review=review
        )
