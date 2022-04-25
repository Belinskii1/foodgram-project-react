from django.shortcuts import render
from rest_framework import filters, viewsets, mixins

from .serializers import UserSerializer
from users.models import User


class UserViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
         queryset = User.objects.all()
         return queryset

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
