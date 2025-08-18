from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import serializers

# Custom JWT token serializers for Swagger documentation
class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField(help_text="JWT access token")
    refresh = serializers.CharField(help_text="JWT refresh token")

class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField(help_text="New JWT access token")

class TokenObtainPairRequestSerializer(serializers.Serializer):
    username = serializers.CharField(help_text="User's username")
    password = serializers.CharField(help_text="User's password", style={'input_type': 'password'})

class TokenRefreshRequestSerializer(serializers.Serializer):
    refresh = serializers.CharField(help_text="JWT refresh token")

# Custom views with Swagger documentation
class DecoratedTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        tags=['api/auth/login/'],
        operation_id='login',
        operation_summary="Login",
        operation_description="Takes a set of user credentials and returns JWT access and refresh tokens",
        request_body=TokenObtainPairRequestSerializer,
        responses={
            200: openapi.Response(
                description="Login successful",
                schema=TokenObtainPairResponseSerializer
            ),
            401: openapi.Response(description="Invalid credentials")
        }
    )
    def post(self, request, *args, **kwargs):
        """
        API endpoint to obtain JWT tokens by providing username and password.
        
        POST:
        Submit username and password to get access and refresh tokens.
        """
        return super().post(request, *args, **kwargs)

class DecoratedTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        tags=['api/auth/login/refresh/'],
        operation_id='refresh_token',
        operation_summary="Refresh Token",
        operation_description="Takes a refresh token and returns a new access token",
        request_body=TokenRefreshRequestSerializer,
        responses={
            200: openapi.Response(
                description="Token refresh successful",
                schema=TokenRefreshResponseSerializer
            ),
            401: openapi.Response(description="Invalid or expired refresh token")
        }
    )
    def post(self, request, *args, **kwargs):
        """
        API endpoint to obtain a new access token using a refresh token.
        
        POST:
        Submit refresh token to get a new access token.
        """
        return super().post(request, *args, **kwargs)