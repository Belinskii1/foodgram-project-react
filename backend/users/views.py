from django.shortcuts import render
from rest_framework import filters, generics, status, viewsets
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Follow, User
from .serializers import FollowListSerializer, UserFollowSerializer


class UserFollowListView(generics.ListAPIView):
    serializer_class = FollowListSerializer
    permission_classes = [IsAuthenticated,]
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        return user.follower.all()


class UserFollowView(generics.CreateAPIView,
                     generics.DestroyAPIView):
    serializer_class = UserFollowSerializer
    permission_classes = [IsAuthenticated,]
