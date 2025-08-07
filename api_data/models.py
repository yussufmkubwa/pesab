from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('default', 'Default'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='default')

class IrrigationEvent(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    duration_minutes = models.IntegerField()
    water_consumed_liters = models.FloatField()
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='irrigation_events')

    def __str__(self):
        return f"Irrigation Event at {self.timestamp} by {self.created_by.username}"

class DeviceReading(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()
    soil_moisture = models.IntegerField() # Percentage 0-100
    device_id = models.CharField(max_length=255, blank=True, null=True) # Optional: to identify specific devices
    # You might want to link this to a specific user or a registered device model
    # For simplicity, let's assume it's just recording data for now.
    # If devices are tied to users, you could add:
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='device_readings', null=True, blank=True)

    def __str__(self):
        return f"Device Reading at {self.timestamp}: Temp={self.temperature}°C, Moisture={self.soil_moisture}%"

class PumpControl(models.Model):
    PUMP_STATUS_CHOICES = [
        ('ON', 'On'),
        ('OFF', 'Off'),
    ]
    control_type_choices = [
        ('MANUAL', 'Manual'),
        ('AUTOMATIC', 'Automatic'),
    ]

    status = models.CharField(max_length=10, choices=PUMP_STATUS_CHOICES, default='OFF')
    control_type = models.CharField(max_length=10, choices=control_type_choices, default='MANUAL')
    timestamp = models.DateTimeField(auto_now_add=True)
    controlled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='pump_controls')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Pump {self.status} ({self.control_type}) at {self.timestamp}"
