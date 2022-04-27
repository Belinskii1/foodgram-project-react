from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers


from .models import User, Follow


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name',
            'last_name', 'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=request.user, following=obj).exists()


class FollowListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    following = serializers.SlugRelatedField(
        required=True,
        queryset=User.objects.all(),
        slug_field='username'
    )
    class Meta:
        model = Follow
        fields = ('user', 'following')
