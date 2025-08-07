from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User, IrrigationEvent, DeviceReading, PumpControl
from .serializers import UserSerializer, IrrigationEventSerializer, DeviceReadingSerializer, PumpControlSerializer

# User Views
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# IrrigationEvent Views
class IrrigationEventListCreateView(generics.ListCreateAPIView):
    queryset = IrrigationEvent.objects.select_related('created_by').all()
    serializer_class = IrrigationEventSerializer
    
    def perform_create(self, serializer):
        serializer.save()

class IrrigationEventRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = IrrigationEvent.objects.select_related('created_by').all()
    serializer_class = IrrigationEventSerializer

# DeviceReading Views
class DeviceReadingListCreateView(generics.ListCreateAPIView):
    queryset = DeviceReading.objects.all()
    serializer_class = DeviceReadingSerializer
    # You might want to add permission_classes here, e.g., IsAuthenticated or a custom permission
    # For simplicity, allowing any for now.

class DeviceReadingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DeviceReading.objects.all()
    serializer_class = DeviceReadingSerializer

# PumpControl Views
class PumpControlListCreateView(generics.ListCreateAPIView):
    queryset = PumpControl.objects.all()
    serializer_class = PumpControlSerializer
    permission_classes = [IsAuthenticated] # Only authenticated users can control the pump

    def perform_create(self, serializer):
        serializer.save(controlled_by=self.request.user)

class PumpControlRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PumpControl.objects.all()
    serializer_class = PumpControlSerializer
    permission_classes = [IsAuthenticated] # Only authenticated users can control the pump
