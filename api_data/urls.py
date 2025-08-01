from django.urls import path
from .views import (
    UserListCreateView,
    UserRetrieveUpdateDestroyView,
    IrrigationEventListCreateView,
    IrrigationEventRetrieveUpdateDestroyView
)

urlpatterns = [
    # User URLs
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),
    
    # IrrigationEvent URLs
    path('irrigation-events/', IrrigationEventListCreateView.as_view(), name='irrigation-event-list-create'),
    path('irrigation-events/<int:pk>/', IrrigationEventRetrieveUpdateDestroyView.as_view(), name='irrigation-event-detail'),
]