from rest_framework import serializers
from .models import User, IrrigationEvent

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                 'address', 'phone_number', 'role', 'date_joined', 'is_active']
        read_only_fields = ['id', 'date_joined']

class IrrigationEventSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    created_by_email = serializers.CharField(source='created_by.email', read_only=True)
    
    class Meta:
        model = IrrigationEvent
        fields = ['id', 'zone_name', 'start_time', 'duration_minutes', 
                 'moisture_level_before', 'moisture_level_after', 'created_by', 
                 'created_by_username', 'created_by_email', 'created_at']
        read_only_fields = ['id', 'created_at', 'created_by_username', 'created_by_email']