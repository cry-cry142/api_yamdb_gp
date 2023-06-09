from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    CategoryViewSet, GenreViewSet, TitleViewSet, ReviewViewSet, CommentViewSet,
    UserViewSet, sign_up, recieve_token
)

app_name = 'api'

router = SimpleRouter()

router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(r'titles/(?P<title_id>[\d]+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>[\d]+)/'
                r'reviews/(?P<review_id>[\d]+)/comments',
                CommentViewSet, basename='comments')
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('v1/auth/signup/', sign_up, name='sign_up'),
    path('v1/auth/token/', recieve_token, name='recieve_token'),
    path(
        'v1/users/me/',
        UserViewSet.as_view({'get': 'retrieve', 'patch': 'update'}),
        kwargs={'username': 'me'}
    ),
    path('v1/', include(router.urls))
]
