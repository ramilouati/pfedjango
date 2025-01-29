from django.urls import path
from django.urls import path
from .views import AllUsers, CustomTokenObtainPairView, RegisterAPIView, UpdateAPIView, UserByCinView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/<str:cin>/', UserByCinView.as_view(), name='user-by-cin'),
    path('updateuser/', UpdateAPIView.as_view(), name='updateuser'),
    path('allusers/', AllUsers.as_view(), name='allusers'),

]