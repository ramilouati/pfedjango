from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework import status
from users.models import CustomUser

from rest_framework.response import Response
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from users.serializer import CustomTokenObtainPairSerializer, UserSerializer

from rest_framework_simplejwt.views import TokenObtainPairView
class SecureAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        return Response({'message': 'This is a secure endpoint!'})

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        print(serializer.objects.all())
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'User created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UpdateAPIView(APIView):

    def post(self, request):
        print(request.data)
        user = CustomUser.objects.get(cin=request.data['cin'])
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class UserByCinView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        cin = self.kwargs.get('cin')
        try:
            user = CustomUser.objects.get(cin=cin)
        except CustomUser.DoesNotExist:
            raise NotFound('User with this CIN not found.')

        serializer = self.get_serializer(user)
        return Response(serializer.data)