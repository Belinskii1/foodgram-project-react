from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, status, views
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


from .models import Tag, Ingredient, Recipe, Favorite
from .serializers import TagSerializer, IngredientSerializer, RecipeSerializer, FavoriteRecipeSerializer
from .filters import IngredientSearchFilter


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RecipesFavoriteViewSet(views.APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request, id):
        data = {'user': request.user.id, 'recipe': id}
        serializer = FavoriteRecipeSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        favorite = get_object_or_404(
            Favorite, user=user, recipe=recipe
        )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
