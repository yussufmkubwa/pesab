from rest_framework import serializers
from .models import User, IrrigationEvent, DeviceReading, PumpControl

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']

class IrrigationEventSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = IrrigationEvent
        fields = '__all__'

class DeviceReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceReading
        fields = '__all__'

class PumpControlSerializer(serializers.ModelSerializer):
    controlled_by = serializers.ReadOnlyField(source='controlled_by.username')

    class Meta:
        model = PumpControl
        fields = '__all__'
