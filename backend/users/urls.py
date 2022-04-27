from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserFollowList

follow_router_v1 = DefaultRouter()


urlpatterns = [
    path('users/subscriptions/', UserFollowList.as_view()),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
]
