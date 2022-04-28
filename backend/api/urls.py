from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import TagViewSet, IngredientViewSet


app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register(r'tags', TagViewSet, basename="tags")
router_v1.register(r'ingredients', IngredientViewSet, basename="ingredients")

urlpatterns = [
    path('', include('users.urls')),
    path('', include(router_v1.urls)),
]
