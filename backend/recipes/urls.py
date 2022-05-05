from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import TagViewSet, IngredientViewSet, RecipeViewSet, RecipesFavoriteViewSet


app_name = 'recipes'

router_v1 = DefaultRouter()

router_v1.register(r'tags', TagViewSet, basename="tags")
router_v1.register(r'ingredients', IngredientViewSet, basename="ingredients")
router_v1.register(r'recipes', RecipeViewSet, basename="recipes")

urlpatterns = [
    path('', include(router_v1.urls)),
]
