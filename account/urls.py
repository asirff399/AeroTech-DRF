from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserRegisterAPIView,UserLoginAPIView,activate

urlpatterns = [
    path('register/', UserRegisterAPIView.as_view(), name='register'),
    path('activate/<uid64>/<token>/', activate, name='activate'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
 