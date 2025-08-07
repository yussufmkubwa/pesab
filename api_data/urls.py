from django.urls import path
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
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
    path('users/me/', CurrentUserView.as_view(), name='current-user-detail'),
    
    # Authentication URLs
    path('login/', obtain_auth_token, name='api-token-auth'), # obtain_auth_token does not need permission_classes=[AllowAny] here, as it's handled by the global settings or its own internal logic.

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
