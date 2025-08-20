from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.utils import swagger_auto_schema
from .views import (
    UserListCreateView,
    UserRetrieveUpdateDestroyView,
    CurrentUserView,
    IrrigationEventListCreateView,
    IrrigationEventRetrieveUpdateDestroyView,
    DeviceReadingListCreateView,
    DeviceReadingRetrieveUpdateDestroyView,
    PumpControlListCreateView,
    PumpControlRetrieveUpdateDestroyView
)
from .iot_views import (
    IoTDeviceReadingView,
    IoTPumpControlListView,
    IoTPumpControlDetailView
)
from .auth_views import DecoratedTokenObtainPairView, DecoratedTokenRefreshView
from .blynk_integration import (
    BlynkTemperatureView,
    BlynkSoilMoistureView, 
    BlynkPumpStatusView,
    BlynkDashboardDataView
)

# Group the URLs by API category
user_management_patterns = [
    path('', UserListCreateView.as_view(), name='user-list-create'),
    path('<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),
]

auth_patterns = [
    path('login/', DecoratedTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', DecoratedTokenRefreshView.as_view(), name='token_refresh'),
    path('me/', CurrentUserView.as_view(), name='current-user'),
]

# Web interface device management patterns
device_patterns = [
    # IrrigationEvent URLs
    path('irrigation-events/', IrrigationEventListCreateView.as_view(), name='irrigation-event-list-create'),
    path('irrigation-events/<int:pk>/', IrrigationEventRetrieveUpdateDestroyView.as_view(), name='irrigation-event-detail'),

    # DeviceReading URLs
    path('readings/', DeviceReadingListCreateView.as_view(), name='device-reading-list-create'),
    path('readings/<int:pk>/', DeviceReadingRetrieveUpdateDestroyView.as_view(), name='device-reading-detail'),

    # PumpControl URLs
    path('pump-control/', PumpControlListCreateView.as_view(), name='pump-control-list-create'),
    path('pump-control/<int:pk>/', PumpControlRetrieveUpdateDestroyView.as_view(), name='pump-control-detail'),
]

# IoT device specific patterns - no authentication required for these endpoints
iot_device_patterns = [
    # DeviceReading endpoint for IoT devices
    path('readings/', IoTDeviceReadingView.as_view(), name='iot-device-reading'),
    
    # PumpControl endpoint for IoT devices
    path('pump-control/', IoTPumpControlListView.as_view(), name='iot-pump-control'),
    path('pump-control/<int:pk>/', IoTPumpControlDetailView.as_view(), name='iot-pump-control-detail'),
]

# Blynk integration patterns
blynk_patterns = [
    path('temperature/', BlynkTemperatureView.as_view(), name='blynk-temperature'),
    path('soil-moisture/', BlynkSoilMoistureView.as_view(), name='blynk-soil-moisture'),
    path('pump-status/', BlynkPumpStatusView.as_view(), name='blynk-pump-status'),
    path('dashboard-data/', BlynkDashboardDataView.as_view(), name='blynk-dashboard-data'),
]

# Main urlpatterns with categorized URLs
urlpatterns = [
    # User Management API - for managing system users
    path('users/', include((user_management_patterns, 'api_data'), namespace='user-management')),
    
    # Authentication API - for handling login, token refresh, and current user info
    path('auth/', include((auth_patterns, 'api_data'), namespace='authentication')),
    
    # Device API - for device readings, irrigation events, and pump control (web interface)
    path('devices/', include((device_patterns, 'api_data'), namespace='device')),
    
    # IoT Device API - dedicated endpoints for IoT devices (no authentication)
    path('iot/', include((iot_device_patterns, 'api_data'), namespace='iot-device')),
    
    # Blynk Integration API - for integrating with Blynk IoT platform
    path('blynk/', include((blynk_patterns, 'api_data'), namespace='blynk-integration')),
    
    # Legacy direct paths for IoT devices - maintained for backward compatibility
    # These should be used by ESP32 devices using the original code
    path('device-readings/', DeviceReadingListCreateView.as_view(), name='legacy-device-readings'),
    path('pump-control/', PumpControlListCreateView.as_view(), name='legacy-pump-control'),
]
