from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny, IsAuthenticated

from recipes.models import Tag, Ingredient
from .serializers import TagSerializer, IngredientSerializer
from .filters import IngredientSearchFilter


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    #filter_backends = (IngredientSearchFilter,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)
