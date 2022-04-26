from django.shortcuts import render
from rest_framework import filters, viewsets, mixins, status, views, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action, api_view, permission_classes

from .serializers import UserSerializer, ChangePasswordSerializer
from users.models import User


class UserViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    #permission_classes = (AllowAny,)

    def get_queryset(self):
        """для списка пользователей"""
        queryset = User.objects.all()
        return queryset

    def perform_create(self, serializer):
        """для создания пользователя"""
        if serializer.is_valid():
            serializer.save()

    def get(self, request, *args, **kwargs):
        """получение профиля конкретного пользователя"""
        return self.retrieve(request, *args, **kwargs)

    def get_me(self, request):
        """получение профиля текущего пользователя"""
        # нужно вынести в отдельную view
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return(self.request.user)


class ChangePasswordView(views.APIView):
    """
    An endpoint for changing password.
    """
    permission_classes = (IsAuthenticated, )

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]}, 
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
