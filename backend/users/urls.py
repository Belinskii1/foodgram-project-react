from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FollowListAPIView, UserFollowApiView

follow_router_v1 = DefaultRouter()


urlpatterns = [
    path('users/subscriptions/', FollowListAPIView.as_view()),
    path('users/<int:id>/subscribe/', UserFollowApiView.as_view(),
         name='subscribe'),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
]
