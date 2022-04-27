from django.shortcuts import render
from rest_framework import filters, generics, status, viewsets
from django.shortcuts import get_object_or_404

from .models import Follow
from .serializers import FollowListSerializer


class UserFollowList(generics.ListAPIView):
    serializer_class = FollowListSerializer
    paginate_by = 10

    def get_queryset(self):
        return Follow.objects.all().filter(user=self.request.user)
