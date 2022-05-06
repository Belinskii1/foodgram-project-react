from django.shortcuts import get_object_or_404
from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Follow, User
from .pagination import UserFollowPagination
from .serializers import FollowListSerializer, UserFollowSerializer


class FollowListAPIView(generics.ListAPIView):
    pagination_class = UserFollowPagination
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user = request.user
        queryset = User.objects.filter(following__user=user)
        page = self.paginate_queryset(queryset)
        serializer = FollowListSerializer(
            page, many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class UserFollowApiView(views.APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, id):
        data = {'user': request.user.id, 'following': id}
        serializer = UserFollowSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, id):
        user = request.user
        following = get_object_or_404(User, id=id)
        follow = get_object_or_404(
            Follow, user=user, following=following
        )
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
