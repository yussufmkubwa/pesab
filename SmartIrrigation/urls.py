# This file defines URL patterns for the SmartIrrigation project.
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from api_data.views import CurrentUserView

# Create schema views for different API categories
schema_view = get_schema_view(
   openapi.Info(
      title="Smart Irrigation API",
      default_version='v1',
      description="""
      # Smart Irrigation API Documentation
      
      The API is organized into the following structure:
      
      ```
      /api/
      ├── users/                # User Management API
      │   ├── ...               # User-related endpoints
      │
      ├── auth/                 # Authentication API
      │   ├── login/            # JWT token endpoints
      │   ├── login/refresh/    # Token refresh
      │   └── me/               # Current user info
      │
      ├── devices/              # Web Interface Device API
      │   ├── irrigation-events/
      │   ├── readings/         
      │   └── pump-control/
      │
      └── iot/                  # IoT Device API
          ├── readings/         # For sensor readings from IoT devices
          └── pump-control/     # For pump control from IoT devices
      ```
      
      ## User Management API
      APIs for managing system users, including creating, updating, and deleting user accounts.
      
      ## Authentication API
      APIs for user authentication, including login, token refresh, and retrieving current user information.
      
      ## Device API
      APIs for managing device data via web interface: irrigation events, sensor readings, and pump controls.
      
      ## IoT Device API
      APIs specifically designed for IoT devices to send sensor data and retrieve pump control commands.
      These endpoints don't require authentication to allow direct access from ESP32 and other IoT devices.
      """,
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@smartirrigation.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api_data.urls')),
    # Deprecated - now accessible via /api/auth/me/
    path('me/', CurrentUserView.as_view(), name='current-user-detail'),
    
    # API Documentation URLs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
