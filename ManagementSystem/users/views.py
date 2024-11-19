# users/views.py

from rest_framework import status, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserRegistrationSerializer, UserLoginSerializer, TokenSerializer
from django.contrib.auth import authenticate

import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from .signals import user_registered


logger = logging.getLogger('custom')

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    logger.info(f"User {user.username} logged in.")

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    logger.info(f"User {user.username} logged out.")


def register_user(data):
    user = User.objects.create_user(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
    user_registered.send(sender=User, user=user)
    return user


@receiver(user_registered)
def log_user_registration(sender, request, user, **kwargs):
    logger.info(f"User {user.username} registered.")

from django.contrib.auth.models import User
from .signals import user_registered

def register_user(data):
    # Пример создания пользователя
    user = User.objects.create_user(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
    # Отправляем сигнал
    user_registered.send(sender=User, user=user)
    return user


@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # Сохраняем пользователя
            user = serializer.save()

            # Возвращаем данные о зарегистрированном пользователе
            return Response({
                "message": "User created successfully!",
                "user": {
                    "username": user.username,
                    "email": user.email,
                    "role": user.role  # Можно добавить другие поля по необходимости
                }
            }, status=status.HTTP_201_CREATED)

        # Если сериализатор невалиден, возвращаем ошибки
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API для логина пользователя с использованием JWT
@api_view(['POST'])
def login_user(request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                token_serializer = TokenSerializer()
                tokens = token_serializer.get_tokens_for_user(user)
                return Response(tokens, status=status.HTTP_200_OK)
            return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API для обновления роли пользователя
@api_view(['PATCH'])
def update_user_role(request, user_id):
    if request.method == 'PATCH':
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        role = request.data.get('role')
        if role not in ['student', 'teacher', 'admin']:
            return Response({"message": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

        user.role = role
        user.save()
        return Response({"message": "User role updated successfully!"}, status=status.HTTP_200_OK)
