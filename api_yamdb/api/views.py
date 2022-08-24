from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken

from api.serializers import (SignUpSerializer,
                             TokenGetSerializer,
                             UserSerializer)
from api.permissions import IsAdminOnly

from reviews.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdminOnly)
    filter_backends = (SearchFilter, )
    search_fields = ['username', ]

    def perform_create(self, serializer):
        email = self.request.data.get['email']
        if User.objects.filter(email=email):
            return Response('Данная почта уже числится в БЗ',
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()


@api_view(["POST"])
def send_code(request):
    """Получение кода подтверждения на почту для регистрации на проекте."""
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid:
        user = User.objects.create(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
        )
        token = default_token_generator.make_token(user)
        user.token = token
        user.save()
        send_mail(
            'Регистрация пользователя',
            (f'Вы получили код подтверждения регистрации на почтовый адрес.\n'
             f'Почта: {user.email}\n' f'Код подтверждения: {user.token}'),
            f'{settings.EMAIL_FROM}',
            [user.email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def get_token(request):
    """Получение JWT-токена при передаче имени и кода подтверждения."""
    serializer = TokenGetSerializer(data=request.data)
    if serializer.is_valid:
        user = get_object_or_404(User,
                                 username=serializer.validated_data['username']
                                 )
        if serializer.validated_data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
