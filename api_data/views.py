from rest_framework import generics
from rest_framework.response import Response
from .models import User, IrrigationEvent
from .serializers import UserSerializer, IrrigationEventSerializer

# User Views
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

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
