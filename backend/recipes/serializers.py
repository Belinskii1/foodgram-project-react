from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from django.shortcuts import get_object_or_404

from users.serializers import CustomUserSerializer
from .models import (Favorite, Ingredient, IngredientRecipe,
                     Recipe, Tag)


# class TagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tag
#         fields = ('id', 'name', 'color', 'slug')


# class IngredientSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Ingredient
#         fields = ('id', 'name', 'measurement_unit')


# class IngredientQuantitySerializer(serializers.ModelSerializer):
#     id = serializers.ReadOnlyField(source='ingredient.id')
#     name = serializers.ReadOnlyField(source='ingredient.name')
#     measurement_unit = serializers.ReadOnlyField(
#         source='ingredient.measurement_unit'
#     )

#     class Meta:
#         model = IngredientRecipe
#         fields = ('id', 'name', 'measurement_unit', 'amount')


# class RecipeSerializer(serializers.ModelSerializer):
#     tags = TagSerializer(many=True, read_only=True)
#     ingredients = serializers.SerializerMethodField(read_only=True)
#     author = CustomUserSerializer(read_only=True)
#     is_favorited = serializers.SerializerMethodField(read_only=True)
#     is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = Recipe
#         fields = ('id', 'tags', 'ingredients', 'author',
#                   'name', 'image', 'text', 'cooking_time',
#                   'is_favorited', 'is_in_shopping_cart')

#     def get_ingredients(self, obj):
#         ingredients = IngredientRecipe.objects.filter(recipe=obj)
#         return IngredientQuantitySerializer(ingredients, many=True).data

#     def get_is_favorited(self, obj):
#         request = self.context.get('request')
#         if request.user.is_authenticated:
#             return Favorite.objects.filter(user=request.user,
#                                            recipe=obj).exists()

#     def get_is_in_shopping_cart(self, obj):
#         request = self.context.get('request')
#         if request.user.is_authenticated:
#             return ShoppingCart.objects.filter(user=request.user,
#                                                recipe=obj).exists()


# class IngredientWriteSerializer(serializers.ModelSerializer):
#     id = serializers.PrimaryKeyRelatedField(
#         queryset=Ingredient.objects.all()
#     )
#     amount = serializers.IntegerField()

#     class Meta:
#         model = IngredientRecipe
#         fields = ('id', 'amount')


# class RecipeWriteSerializer(serializers.ModelSerializer):
#     image = Base64ImageField()
#     ingredients = IngredientWriteSerializer(many=True)
#     tags = serializers.PrimaryKeyRelatedField(
#         queryset=Tag.objects.all(), many=True
#     )
#     author = CustomUserSerializer(read_only=True)

#     class Meta:
#         model = Recipe
#         fields = ('image', 'ingredients', 'tags',
#                   'author', 'name', 'text', 'cooking_time')

#     def validate(self, data):
#         ingredients = self.initial_data.get('ingredients')
#         if not ingredients:
#             raise serializers.ValidationError({
#                 'Нужно выбрать хотя бы один ингредиент!'
#             })
#         ingredients_list = []
#         for ingredient in ingredients:
#             ingredient_id = ingredient['id']
#             if ingredient_id in ingredients_list:
#                 raise serializers.ValidationError({
#                     'Ингридиенты повторяются!'
#                 })
#             ingredients_list.append(ingredient_id)
#             amount = ingredient['amount']
#             if int(amount) <= 0:
#                 raise serializers.ValidationError({
#                     'Укажите хотя бы один ингридиент!'
#                 })
#         tags = self.initial_data.get('tags')
#         if not tags:
#             raise serializers.ValidationError({
#                 'Нужно выбрать хотя бы один тэг!'
#             })
#         tags_list = []
#         for tag in tags:
#             if tag in tags_list:
#                 raise serializers.ValidationError({
#                     'Тэги должны быть уникальными!'
#                 })
#             tags_list.append(tag)

#         cooking_time = self.initial_data.get('cooking_time')
#         if int(cooking_time) <= 0:
#             raise serializers.ValidationError({
#                 'Время приготовления должно быть больше 0!'
#             })
#         return data

#     def create_ingredients(self, ingredients, recipe):
#         for ingredient in ingredients:
#             ingredient_id = ingredient['id']
#             amount = ingredient['amount']
#             IngredientRecipe.objects.create(
#                 recipe=recipe, ingredient=ingredient_id, amount=amount
#             )

#     def create_tags(self, tags, recipe):
#         for tag in tags:
#             recipe.tags.add(tag)

#     def create(self, validated_data):
#         author = self.context.get('request').user
#         tags = validated_data.pop('tags')
#         ingredients = validated_data.pop('ingredients')
#         recipe = Recipe.objects.create(author=author, **validated_data)
#         self.create_tags(tags, recipe)
#         self.create_ingredients(ingredients, recipe)
#         return recipe

#     def update(self, instance, validated_data):
#         instance.image = validated_data.get('image', instance.image)
#         instance.name = validated_data.get('name', instance.name)
#         instance.text = validated_data.get('text', instance.text)
#         instance.cooking_time = validated_data.get(
#             'cooking_time', instance.cooking_time
#         )

#         instance.tags.clear()
#         tags = validated_data.get('tags')
#         self.create_tags(tags, instance)

#         IngredientRecipe.objects.filter(recipe=instance).all().delete()
#         ingredients = validated_data.get('ingredients')
#         self.create_ingredients(ingredients, instance)

#         instance.save()
#         return instance

#     def to_representation(self, instance):
#         request = self.context.get('request')
#         context = {'request': request}
#         return RecipeSerializer(
#             instance, context=context).data


# class RecipeRepresentationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Recipe
#         fields = ('id', 'name', 'image', 'cooking_time')


# class FavoriteRecipeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Favorite
#         fields = ('user', 'recipe')

#     def validate(self, data):
#         request = self.context.get('request')
#         if not request or request.user.is_anonymous:
#             return False
#         recipe = data['recipe']
#         if Favorite.objects.filter(
#             user=request.user,
#             recipe=recipe
#         ).exists():
#             raise serializers.ValidationError({
#                 'recipe': 'Вы уже добавили этот рецепт в избранное!'
#             })
#         return data

#     def to_representation(self, instance):
#         request = self.context.get('request')
#         context = {'request': request}
#         return RecipeRepresentationSerializer(
#             instance.recipe, context=context).data


# class ShoppingCartSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ShoppingCart
#         fields = ('user', 'recipe')

#     def validate(self, data):
#         request = self.context.get('request')
#         if not request or request.user.is_anonymous:
#             return False
#         recipe = data['recipe']
#         if ShoppingCart.objects.filter(
#             user=request.user,
#             recipe=recipe
#         ).exists():
#             raise serializers.ValidationError({
#                 'recipe': 'Вы уже добавили этот рецепт рецепт в корзину!'
#             })
#         return data

#     def to_representation(self, instance):
#         request = self.context.get('request')
#         context = {'request': request}
#         return RecipeRepresentationSerializer(
#             instance.recipe, context=context).data

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeIngredientSerializers(serializers.ModelSerializer):
    name = serializers.CharField(source="ingredient.name")
    measurement_unit = serializers.CharField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')
        read_only_fields = ("id", "name", "measurement_unit", "amount")


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientSerializers(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text',
            'cooking_time'
        )
        model = Recipe

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(favorites__user=user, id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(shoppingcart__user=user, id=obj.id).exists()

    def create(self, validated_data):
        request = self.context.get('request')
        ingredients = self.initial_data.get('ingredients')
        tags_data = self.initial_data.get('tags')
        recipe = Recipe.objects.create(
            author=request.user,
            **validated_data
        )
        recipe.tags.set(tags_data)
        for ingredient in ingredients:
            amount = ingredient.get('amount')
            ingredient_instance = get_object_or_404(
                Ingredient,
                pk=ingredient.get('id')
            )
            IngredientRecipe.objects.create(
                recipe=recipe,
                ingredient=ingredient_instance,
                amount=amount
            )
        recipe.save()
        return recipe

    def update(self, instance, validated_data):
        ingredients = self.initial_data.get('ingredients')
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.tags.clear()
        tags_data = self.initial_data.get('tags')
        instance.tags.set(tags_data)
        IngredientRecipe.objects.filter(recipe=instance).all().delete()
        for ingredient in ingredients:
            IngredientRecipe.objects.create(
                recipe=instance,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'),
            )
        instance.save()
        return instance


class FavoriteSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(source='recipe.id')
    name = serializers.CharField(source='recipe.name')
    image = Base64ImageField(source='recipe.image')
    cooking_time = serializers.IntegerField(source='recipe.cooking_time')

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Favorite


class CropRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')
