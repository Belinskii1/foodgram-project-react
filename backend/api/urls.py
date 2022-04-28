from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import TagsViewSet


app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register(r'tags', TagsViewSet, basename="tags")

urlpatterns = [
    path('', include('users.urls')),
    path('', include(router_v1.urls)),
]
