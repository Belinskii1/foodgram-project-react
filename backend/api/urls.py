from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet, MyTokenObtainPairView

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register(r'users', UserViewSet, basename='users')

auth_urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]

urlpatterns = [
    path('', include(router_v1.urls)),
    re_path(r'^/users/(?P<pk>\d+)/', UserViewSet.as_view({'get': 'retrieve'}), name='user_detail'),
    path('users/me/', UserViewSet.as_view({'get': 'retrieve'}), name='user_me'),
    path('auth/token/', include(auth_urlpatterns)),

]
