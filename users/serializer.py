from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.serializers import ModelSerializer
from users.models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['cin', 'tel', 'nom', 'prenom', 'date_naissance', 'address', 'date_permis', 'password', 'npermis','role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'User created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AllUsers(APIView):
    def get(self):
        serializer = UserSerializer(CustomUser.objects.all(), many=True)
        print(serializer.objects.all())
        return Response(serializer.data)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    cin = serializers.CharField()
    tel = serializers.CharField()

    def validate(self, attrs):
        # Get the cin and tel from the request
        cin = attrs.get('cin')
        tel = attrs.get('tel')
        print("fffffffffffff")

        try:
            # Find user by cin and tel
            print(CustomUser.objects.all())
            user = CustomUser.objects.get(cin=cin, tel=tel)
            print(user)
            print("eeeeeeeeeeeee")
        except CustomUser.DoesNotExist:
            print("fffffffffffff")
            raise serializers.ValidationError('No user found with provided credentials.')

        # Check the password if provided
        # password = attrs.get('password')
        # if not user.check_password(password):
        #     raise serializers.ValidationError('Incorrect password.')

        # Use the default validation provided by TokenObtainPairSerializer
        # data = super().validate({
        #     'username': user.username,  # Internally passing username for token creation
            
        # })

        # # Add additional user details to the response
        # data['user'] = {
        #     'user_id': user.id,
        #     'cin': user.cin,
        #     'tel': user.tel,
        #     'first_name': user.first_name,
        #     'last_name': user.last_name,
        #     'email': user.email,
        # }

        return "data"

    
# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         print("eeeeeeeeeeeee")
#         # Allow login with 'cin' instead of 'username'
#         username = attrs.get("cin", None)
#         password = attrs.get("password", None)
#         print(username, password)

#         # Validate using the parent method
#         return super().validate(attrs)