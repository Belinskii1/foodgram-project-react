from django.shortcuts import render
from rest_framework import filters, viewsets, mixins, status, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView


from .serializers import UserSerializer, MyTokenObtainPairSerializer
from users.models import User


class UserViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        """переопредлеяет набор запросов"""
        queryset = User.objects.all()
        return queryset

    def perform_create(self, serializer):
        """переопределяем создание"""
        if serializer.is_valid():
            serializer.save()

    def get(self, request, *args, **kwargs):
        """получение профиля конкретного пользователя"""
        return self.retrieve(request, *args, **kwargs)

    def get_me(self, request):
        """получение профиля текущего пользователя"""
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return(self.request.user)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
