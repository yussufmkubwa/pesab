from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('farmer', 'Farmer'),
    )
    
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='farmer')
    
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',
        blank=True,
    )
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    def __str__(self):
        return self.username

class IrrigationEvent(models.Model):
    zone_name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField()
    moisture_level_before = models.FloatField()
    moisture_level_after = models.FloatField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='irrigation_events')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Irrigation in {self.zone_name} at {self.start_time.strftime('%Y-%m-%d %H:%M')} by {self.created_by.username}"
