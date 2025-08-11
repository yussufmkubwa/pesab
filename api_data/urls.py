from django.urls import path
from django.urls import path
from .custom_auth import CustomAuthToken
from rest_framework.permissions import AllowAny # Import AllowAny
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

urlpatterns = [
    # User URLs
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),
    
    
    # Authentication URLs
    path('login/', CustomAuthToken.as_view(), name='api-token-auth'),

    # IrrigationEvent URLs
    path('irrigation-events/', IrrigationEventListCreateView.as_view(), name='irrigation-event-list-create'),
    path('irrigation-events/<int:pk>/', IrrigationEventRetrieveUpdateDestroyView.as_view(), name='irrigation-event-detail'),

    # DeviceReading URLs
    path('device-readings/', DeviceReadingListCreateView.as_view(), name='device-reading-list-create'),
    path('device-readings/<int:pk>/', DeviceReadingRetrieveUpdateDestroyView.as_view(), name='device-reading-detail'),

    # PumpControl URLs
    path('pump-control/', PumpControlListCreateView.as_view(), name='pump-control-list-create'),
    path('pump-control/<int:pk>/', PumpControlRetrieveUpdateDestroyView.as_view(), name='pump-control-detail'),
]
