from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import serializers

class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class CustomAuthToken(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    
    @swagger_auto_schema(
        request_body=AuthTokenSerializer,
        responses={
            200: openapi.Response(
                description="Successful authentication",
                examples={
                    "application/json": {
                        "token": "your-auth-token",
                        "user_id": 1,
                        "email": "user@example.com",
                        "role": "farmer"
                    }
                }
            ),
            400: "Invalid credentials or device ID mismatch"
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        #user = serializer.validated_data['user']
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = User.objects.get(username=username)

        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect credentials")

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'role': user.role
        })
