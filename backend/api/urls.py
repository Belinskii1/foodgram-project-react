from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet, ChangePasswordView
from authsystem.views import MyTokenObtainPairView, APILogoutView

app_name = 'api'

router_v1 = DefaultRouter()

#router_v1.register(r'users', UserViewSet, basename='users')

auth_urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', APILogoutView.as_view(), name='auth_logout'),
]

urlpatterns = [
    #path('', include(router_v1.urls)),
    path('', include('users.urls')),
    #re_path(r'^/users/(?P<pk>\d+)/', UserViewSet.as_view({'get': 'retrieve'}), name='user_detail'),
    #path('users/me/', UserViewSet.as_view({'get': 'retrieve'}), name='user_me'),
    #path('users/set_password/', ChangePasswordView.as_view(), name='set_password'),
    #path('auth/token/', include(auth_urlpatterns)),
]
