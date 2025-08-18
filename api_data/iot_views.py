from rest_framework import generics
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import DeviceReading, PumpControl
from .serializers import DeviceReadingSerializer, PumpControlSerializer

# IoT Device API views - specifically tagged for IoT device documentation
@swagger_auto_schema(
    tags=['api/iot/readings/'],
    operation_id='iot_readings',
    operation_summary="IoT Device Readings",
    operation_description="API endpoints for IoT devices to submit sensor readings",
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
class IoTDeviceReadingView(generics.ListCreateAPIView):
    """
    API endpoint for IoT devices to submit sensor readings.
    This endpoint is specifically designed for ESP32 and other IoT devices.
    
    GET:
    Retrieve a list of all sensor readings.
    
    POST:
    Submit a new sensor reading from an IoT device with temperature and soil moisture data.
    No authentication required for this endpoint.
    """
    queryset = DeviceReading.objects.all()
    serializer_class = DeviceReadingSerializer
    permission_classes = [] # No authentication required for IoT devices


@swagger_auto_schema(
    tags=['api/iot/pump-control/'],
    operation_id='iot_pump_control_list',
    operation_summary="IoT Pump Control List",
    operation_description="API endpoints for IoT devices to get pump control commands",
    responses={
        200: openapi.Response(
            description="List of pump control commands (newest first)",
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
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
            )
        ),
    }
)
class IoTPumpControlListView(generics.ListCreateAPIView):
    """
    API endpoint for IoT devices to get pump control commands.
    This endpoint is specifically designed for ESP32 and other IoT devices.
    
    GET:
    Retrieve the latest pump control commands. IoT devices should use the most recent command.
    
    POST:
    Submit a new pump control command from an IoT device.
    """
    queryset = PumpControl.objects.all().order_by('-timestamp')  # Sort by timestamp descending to get latest first
    serializer_class = PumpControlSerializer
    permission_classes = []  # No authentication required for IoT devices

    def perform_create(self, serializer):
        # IoT devices don't have authentication
        serializer.save(controlled_by=None)


@swagger_auto_schema(
    tags=['api/iot/pump-control/'],
    operation_id='iot_pump_control_detail',
    operation_summary="IoT Pump Control Detail",
    operation_description="API endpoints for IoT devices to manage specific pump control commands",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'status': openapi.Schema(type=openapi.TYPE_STRING, enum=['ON', 'OFF'], description='Pump status (ON/OFF)'),
            'control_type': openapi.Schema(type=openapi.TYPE_STRING, enum=['MANUAL', 'AUTOMATIC'], description='Control type (MANUAL/AUTOMATIC)'),
            'notes': openapi.Schema(type=openapi.TYPE_STRING, description='Optional notes about the pump control action'),
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
                    'notes': openapi.Schema(type=openapi.TYPE_STRING, description='Notes about the control action'),
                }
            )
        ),
        204: openapi.Response(description="Pump control command deleted successfully"),
        404: openapi.Response(description="Pump control command not found"),
    }
)
class IoTPumpControlDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for IoT devices to manage specific pump control commands.
    This endpoint is specifically designed for ESP32 and other IoT devices.
    
    GET:
    Retrieve a specific pump control command by ID.
    
    PUT/PATCH:
    Update a specific pump control command by ID.
    
    DELETE:
    Delete a specific pump control command by ID.
    """
    queryset = PumpControl.objects.all()
    serializer_class = PumpControlSerializer
    permission_classes = []  # No authentication required for IoT devices