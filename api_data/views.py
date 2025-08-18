from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import User, IrrigationEvent, DeviceReading, PumpControl
from .serializers import UserSerializer, IrrigationEventSerializer, DeviceReadingSerializer, PumpControlSerializer

# User Management Views
@swagger_auto_schema(
    tags=['api/users/'],
    operation_id='user_list_create',
    operation_summary="List and Create Users",
    operation_description="API endpoints for listing and creating users",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'password', 'email', 'role'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username for the new user'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, description='Password for the new user'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description='Email address'),
            'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First name'),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last name'),
            'role': openapi.Schema(type=openapi.TYPE_STRING, enum=['admin', 'farmer'], description='User role (admin or farmer)'),
        }
    ),
    responses={
        201: openapi.Response(
            description="User created successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID'),
                    'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                    'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address'),
                    'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First name'),
                    'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last name'),
                    'role': openapi.Schema(type=openapi.TYPE_STRING, description='User role'),
                }
            )
        ),
        400: openapi.Response(description="Bad request"),
        401: openapi.Response(description="Authentication credentials not provided")
    }
)
class UserListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing all users and creating new users.
    
    GET: 
    List all users in the system.
    
    POST:
    Create a new user with username, password, email, and role.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

@swagger_auto_schema(
    tags=['api/auth/me/'],
    operation_id='current_user',
    operation_summary="Current User",
    operation_description="API endpoint to retrieve current authenticated user information",
    responses={
        200: openapi.Response(
            description="Current user information retrieved successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID'),
                    'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                    'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address'),
                    'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First name'),
                    'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last name'),
                    'role': openapi.Schema(type=openapi.TYPE_STRING, description='User role (admin or farmer)'),
                }
            )
        ),
        401: openapi.Response(description="Authentication credentials not provided"),
    },
    security=[{'Bearer': []}]
)
class CurrentUserView(generics.RetrieveAPIView):
    """
    API endpoint to get the current authenticated user's details.
    
    GET:
    Returns information about the currently authenticated user based on the JWT token provided.
    Requires a valid authentication token in the Authorization header.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

@swagger_auto_schema(
    tags=['api/users/'],
    operation_id='user_detail',
    operation_summary="Get, Update or Delete User",
    operation_description="API endpoint for retrieving, updating, or deleting a specific user",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username for the user'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description='Email address'),
            'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First name'),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last name'),
            'role': openapi.Schema(type=openapi.TYPE_STRING, enum=['admin', 'farmer'], description='User role (admin or farmer)'),
        }
    ),
    responses={
        200: openapi.Response(
            description="User details retrieved/updated successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID'),
                    'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                    'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address'),
                    'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First name'),
                    'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last name'),
                    'role': openapi.Schema(type=openapi.TYPE_STRING, description='User role'),
                }
            )
        ),
        204: openapi.Response(description="User deleted successfully"),
        400: openapi.Response(description="Bad request"),
        401: openapi.Response(description="Authentication credentials not provided"),
        404: openapi.Response(description="User not found"),
    },
    security=[{'Bearer': []}]
)
class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to get, update or delete a specific user.
    
    GET:
    Retrieve details of a specific user by ID.
    
    PUT:
    Update all fields of a user by ID.
    
    PATCH:
    Partially update a user by ID.
    
    DELETE:
    Delete a user by ID.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Device API - Irrigation Event Views
@swagger_auto_schema(
    tags=['api/devices/irrigation-events/'],
    operation_description="API endpoints for listing and creating irrigation events",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['duration_minutes', 'water_consumed_liters'],
        properties={
            'duration_minutes': openapi.Schema(type=openapi.TYPE_INTEGER, description='Duration of irrigation in minutes'),
            'water_consumed_liters': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description='Amount of water consumed in liters'),
            'notes': openapi.Schema(type=openapi.TYPE_STRING, description='Optional notes about the irrigation event'),
        }
    ),
    responses={
        201: openapi.Response(
            description="Irrigation event created successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Event ID'),
                    'timestamp': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Timestamp of the irrigation event'),
                    'duration_minutes': openapi.Schema(type=openapi.TYPE_INTEGER, description='Duration in minutes'),
                    'water_consumed_liters': openapi.Schema(type=openapi.TYPE_NUMBER, description='Water consumed in liters'),
                    'notes': openapi.Schema(type=openapi.TYPE_STRING, description='Notes about the irrigation event'),
                    'created_by': openapi.Schema(type=openapi.TYPE_STRING, description='Username of the creator'),
                }
            )
        ),
        400: openapi.Response(description="Bad request"),
        401: openapi.Response(description="Authentication credentials not provided"),
    },
    security=[{'Bearer': []}]
)
class IrrigationEventListCreateView(generics.ListCreateAPIView):
    """
    API endpoint to list all irrigation events and create new irrigation events.
    
    GET:
    List all irrigation events in the system.
    
    POST:
    Create a new irrigation event with duration and water consumed data.
    """
    queryset = IrrigationEvent.objects.select_related('created_by').all()
    serializer_class = IrrigationEventSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

@swagger_auto_schema(
    tags=['api/devices/irrigation-events/{id}/'],
    operation_description="API endpoints for retrieving, updating, or deleting irrigation events",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'duration_minutes': openapi.Schema(type=openapi.TYPE_INTEGER, description='Duration of irrigation in minutes'),
            'water_consumed_liters': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description='Amount of water consumed in liters'),
            'notes': openapi.Schema(type=openapi.TYPE_STRING, description='Optional notes about the irrigation event'),
        }
    ),
    responses={
        200: openapi.Response(
            description="Irrigation event retrieved/updated successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Event ID'),
                    'timestamp': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Timestamp of the irrigation event'),
                    'duration_minutes': openapi.Schema(type=openapi.TYPE_INTEGER, description='Duration in minutes'),
                    'water_consumed_liters': openapi.Schema(type=openapi.TYPE_NUMBER, description='Water consumed in liters'),
                    'notes': openapi.Schema(type=openapi.TYPE_STRING, description='Notes about the irrigation event'),
                    'created_by': openapi.Schema(type=openapi.TYPE_STRING, description='Username of the creator'),
                }
            )
        ),
        204: openapi.Response(description="Irrigation event deleted successfully"),
        400: openapi.Response(description="Bad request"),
        401: openapi.Response(description="Authentication credentials not provided"),
        404: openapi.Response(description="Irrigation event not found"),
    },
    security=[{'Bearer': []}]
)
class IrrigationEventRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to get, update or delete a specific irrigation event.
    
    GET:
    Retrieve details of a specific irrigation event by ID.
    
    PUT:
    Update all fields of an irrigation event by ID.
    
    PATCH:
    Partially update an irrigation event by ID.
    
    DELETE:
    Delete an irrigation event by ID.
    """
    queryset = IrrigationEvent.objects.select_related('created_by').all()
    serializer_class = IrrigationEventSerializer
    permission_classes = [IsAuthenticated]

# Device API - Device Reading Views
@swagger_auto_schema(
    tags=['api/devices/readings/'],
    operation_description="API endpoints for listing and creating device sensor readings",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['temperature', 'soil_moisture'],
        properties={
            'temperature': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description='Temperature reading in Celsius'),
            'soil_moisture': openapi.Schema(type=openapi.TYPE_INTEGER, description='Soil moisture level as percentage (0-100)'),
            'device_id': openapi.Schema(type=openapi.TYPE_STRING, description='Optional identifier for the specific device'),
        }
    ),
    responses={
        201: openapi.Response(
            description="Device reading created successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Reading ID'),
                    'timestamp': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Timestamp of the reading'),
                    'temperature': openapi.Schema(type=openapi.TYPE_NUMBER, description='Temperature in Celsius'),
                    'soil_moisture': openapi.Schema(type=openapi.TYPE_INTEGER, description='Soil moisture percentage'),
                    'device_id': openapi.Schema(type=openapi.TYPE_STRING, description='Device identifier'),
                }
            )
        ),
        400: openapi.Response(description="Bad request - Invalid reading data"),
    }
)
class DeviceReadingListCreateView(generics.ListCreateAPIView):
    """
    API endpoint to list all device sensor readings and create new readings.
    This endpoint is used to collect data from soil moisture sensors, temperature sensors, etc.
    
    GET:
    List all sensor readings in the system.
    
    POST:
    Submit a new sensor reading with temperature and soil moisture data.
    Note: This endpoint does NOT require authentication to allow IoT devices to submit data.
    """
    queryset = DeviceReading.objects.all()
    serializer_class = DeviceReadingSerializer
    permission_classes = [] # Explicitly allow unauthenticated access to receive data from IoT devices

@swagger_auto_schema(
    tags=['api/devices/readings/{id}/'],
    operation_description="API endpoints for retrieving, updating, or deleting device sensor readings",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'temperature': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description='Temperature reading in Celsius'),
            'soil_moisture': openapi.Schema(type=openapi.TYPE_INTEGER, description='Soil moisture level as percentage (0-100)'),
            'device_id': openapi.Schema(type=openapi.TYPE_STRING, description='Optional identifier for the specific device'),
        }
    ),
    responses={
        200: openapi.Response(
            description="Device reading retrieved/updated successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Reading ID'),
                    'timestamp': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Timestamp of the reading'),
                    'temperature': openapi.Schema(type=openapi.TYPE_NUMBER, description='Temperature in Celsius'),
                    'soil_moisture': openapi.Schema(type=openapi.TYPE_INTEGER, description='Soil moisture percentage'),
                    'device_id': openapi.Schema(type=openapi.TYPE_STRING, description='Device identifier'),
                }
            )
        ),
        204: openapi.Response(description="Device reading deleted successfully"),
        400: openapi.Response(description="Bad request"),
        404: openapi.Response(description="Device reading not found"),
    },
    security=[{'Bearer': []}]
)
class DeviceReadingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to get, update or delete a specific device sensor reading.
    
    GET:
    Retrieve details of a specific sensor reading by ID.
    
    PUT:
    Update all fields of a sensor reading by ID.
    
    PATCH:
    Partially update a sensor reading by ID.
    
    DELETE:
    Delete a sensor reading by ID.
    
    Note: While creating readings doesn't require authentication, 
    managing existing readings requires authentication.
    """
    queryset = DeviceReading.objects.all()
    serializer_class = DeviceReadingSerializer
    permission_classes = [IsAuthenticated]

# Device API - Pump Control Views
@swagger_auto_schema(
    tags=['api/devices/pump-control/'],
    operation_description="API endpoints for listing and creating pump control commands",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['status'],
        properties={
            'status': openapi.Schema(type=openapi.TYPE_STRING, enum=['ON', 'OFF'], description='Pump status (ON/OFF)'),
            'control_type': openapi.Schema(type=openapi.TYPE_STRING, enum=['MANUAL', 'AUTOMATIC'], description='Control type (MANUAL/AUTOMATIC)'),
            'notes': openapi.Schema(type=openapi.TYPE_STRING, description='Optional notes about the pump control action'),
            'device_id': openapi.Schema(type=openapi.TYPE_STRING, description='Optional identifier for the specific device'),
        }
    ),
    responses={
        201: openapi.Response(
            description="Pump control command created successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Command ID'),
                    'status': openapi.Schema(type=openapi.TYPE_STRING, description='Pump status (ON/OFF)'),
                    'control_type': openapi.Schema(type=openapi.TYPE_STRING, description='Control type (MANUAL/AUTOMATIC)'),
                    'timestamp': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Timestamp of the command'),
                    'controlled_by': openapi.Schema(type=openapi.TYPE_STRING, description='Username of the controller'),
                    'notes': openapi.Schema(type=openapi.TYPE_STRING, description='Notes about the control action'),
                }
            )
        ),
        400: openapi.Response(description="Bad request"),
    }
)
class PumpControlListCreateView(generics.ListCreateAPIView):
    """
    API endpoint to list all pump control commands and create new commands.
    This endpoint allows users to control irrigation pumps by sending on/off commands.
    
    GET:
    List all pump control commands in the system.
    IoT devices can retrieve the current pump status.
    
    POST:
    Create a new pump control command to turn the pump ON or OFF.
    Can be used by both web interface users and IoT devices.
    """
    queryset = PumpControl.objects.all().order_by('-timestamp')  # Sort by timestamp descending to get latest first
    serializer_class = PumpControlSerializer
    permission_classes = []  # Allow IoT devices to access without authentication

    def perform_create(self, serializer):
        # If authenticated, use the authenticated user
        if self.request.user.is_authenticated:
            serializer.save(controlled_by=self.request.user)
        else:
            # For IoT devices or other non-authenticated requests
            serializer.save(controlled_by=None)

@swagger_auto_schema(
    tags=['api/devices/pump-control/{id}/'],
    operation_description="API endpoints for retrieving, updating, or deleting pump control commands",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'status': openapi.Schema(type=openapi.TYPE_STRING, enum=['ON', 'OFF'], description='Pump status (ON/OFF)'),
            'control_type': openapi.Schema(type=openapi.TYPE_STRING, enum=['MANUAL', 'AUTOMATIC'], description='Control type (MANUAL/AUTOMATIC)'),
            'notes': openapi.Schema(type=openapi.TYPE_STRING, description='Optional notes about the pump control action'),
            'device_id': openapi.Schema(type=openapi.TYPE_STRING, description='Optional identifier for the specific device'),
        }
    ),
    responses={
        200: openapi.Response(
            description="Pump control command retrieved/updated successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Command ID'),
                    'status': openapi.Schema(type=openapi.TYPE_STRING, description='Pump status (ON/OFF)'),
                    'control_type': openapi.Schema(type=openapi.TYPE_STRING, description='Control type (MANUAL/AUTOMATIC)'),
                    'timestamp': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Timestamp of the command'),
                    'controlled_by': openapi.Schema(type=openapi.TYPE_STRING, description='Username of the controller'),
                    'notes': openapi.Schema(type=openapi.TYPE_STRING, description='Notes about the control action'),
                }
            )
        ),
        204: openapi.Response(description="Pump control command deleted successfully"),
        400: openapi.Response(description="Bad request"),
        404: openapi.Response(description="Pump control command not found"),
    }
)
class PumpControlRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to get, update or delete a specific pump control command.
    
    GET:
    Retrieve details of a specific pump control command by ID.
    
    PUT:
    Update all fields of a pump control command by ID.
    
    PATCH:
    Partially update a pump control command by ID.
    
    DELETE:
    Delete a pump control command by ID.
    
    No authentication required - IoT devices can access these endpoints.
    """
    queryset = PumpControl.objects.all()
    serializer_class = PumpControlSerializer
    permission_classes = []  # Allow IoT devices to access without authentication
