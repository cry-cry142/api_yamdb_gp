from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .serializers import SignUpSerializer

User = get_user_model()


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        user, _ = User.objects.get_or_create(**serializer.validated_data)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Регистрация на сервисе YamDB прошла успешно!',
            message=f'Ваш персональный код подтверждения: {confirmation_code}',
            recipient_list=[user.email],
            fail_silently=False
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
