import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Blynk configuration
BLYNK_TOKEN = "oM1I_kX96wCPnfZe5vM8xTmzy84hW65p"
BLYNK_BASE = "https://blynk.cloud/external/api"

class BlynkIntegration:
    """
    Utility class for Blynk API integration
    """
    @staticmethod
    def get_pin_value(vpin):
        """Get value from Blynk virtual pin"""
        url = f"{BLYNK_BASE}/get?token={BLYNK_TOKEN}&pin={vpin}"
        response = requests.get(url)
        if response.status_code == 200:
            value = response.json()[0]  # Blynk returns list of values
            return value
        return None

    @staticmethod
    def set_pin_value(vpin, value):
        """Set value to Blynk virtual pin"""
        url = f"{BLYNK_BASE}/update?token={BLYNK_TOKEN}&pin={vpin}&value={value}"
        response = requests.get(url)
        return response.status_code == 200

# API Views for Blynk integration
class BlynkTemperatureView(APIView):
    """
    API endpoint to get temperature data from Blynk
    """
    @swagger_auto_schema(
        tags=['api/blynk/temperature/'],
        operation_id='blynk_temperature',
        operation_summary="Get Temperature from Blynk",
        operation_description="Gets the temperature value from Blynk IoT platform",
        responses={
            200: openapi.Response(
                description="Temperature retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'temperature': openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            description='Temperature value from Blynk (V0)'
                        ),
                        'timestamp': openapi.Schema(
                            type=openapi.TYPE_STRING, 
                            format=openapi.FORMAT_DATETIME,
                            description='Timestamp of the request'
                        ),
                    }
                )
            ),
            503: openapi.Response(description="Blynk service unavailable")
        }
    )
    def get(self, request):
        """
        Get temperature value from Blynk
        """
        temp = BlynkIntegration.get_pin_value("V0")
        
        if temp is not None:
            from datetime import datetime
            return Response({
                'temperature': float(temp) if temp is not None else None,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return Response(
                {"error": "Failed to retrieve data from Blynk"}, 
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


class BlynkSoilMoistureView(APIView):
    """
    API endpoint to get soil moisture data from Blynk
    """
    @swagger_auto_schema(
        tags=['api/blynk/soil-moisture/'],
        operation_id='blynk_soil_moisture',
        operation_summary="Get Soil Moisture from Blynk",
        operation_description="Gets the soil moisture value from Blynk IoT platform",
        responses={
            200: openapi.Response(
                description="Soil moisture retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'soil_moisture': openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            description='Soil moisture value from Blynk (V1)'
                        ),
                        'timestamp': openapi.Schema(
                            type=openapi.TYPE_STRING, 
                            format=openapi.FORMAT_DATETIME,
                            description='Timestamp of the request'
                        ),
                    }
                )
            ),
            503: openapi.Response(description="Blynk service unavailable")
        }
    )
    def get(self, request):
        """
        Get soil moisture value from Blynk
        """
        soil = BlynkIntegration.get_pin_value("V1")
        
        if soil is not None:
            from datetime import datetime
            return Response({
                'soil_moisture': float(soil) if soil is not None else None,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return Response(
                {"error": "Failed to retrieve data from Blynk"}, 
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


class BlynkPumpStatusView(APIView):
    """
    API endpoint to get and set pump status on Blynk
    """
    @swagger_auto_schema(
        tags=['api/blynk/pump-status/'],
        operation_id='blynk_pump_status_get',
        operation_summary="Get Pump Status from Blynk",
        operation_description="Gets the pump status from Blynk IoT platform",
        responses={
            200: openapi.Response(
                description="Pump status retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'pump_status': openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description='Pump status from Blynk (V2): 1=ON, 0=OFF'
                        ),
                        'timestamp': openapi.Schema(
                            type=openapi.TYPE_STRING, 
                            format=openapi.FORMAT_DATETIME,
                            description='Timestamp of the request'
                        ),
                    }
                )
            ),
            503: openapi.Response(description="Blynk service unavailable")
        }
    )
    def get(self, request):
        """
        Get pump status from Blynk
        """
        pump = BlynkIntegration.get_pin_value("V2")
        
        if pump is not None:
            from datetime import datetime
            return Response({
                'pump_status': int(pump) if pump is not None else None,
                'is_on': bool(int(pump)) if pump is not None else None,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return Response(
                {"error": "Failed to retrieve data from Blynk"}, 
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

    @swagger_auto_schema(
        tags=['api/blynk/pump-status/'],
        operation_id='blynk_pump_status_set',
        operation_summary="Set Pump Status in Blynk",
        operation_description="Sets the pump status in Blynk IoT platform",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['status'],
            properties={
                'status': openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    description='Pump status to set: true=ON, false=OFF'
                ),
            }
        ),
        responses={
            200: openapi.Response(
                description="Pump status updated successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Success status'),
                        'pump_status': openapi.Schema(type=openapi.TYPE_INTEGER, description='Pump status: 1=ON, 0=OFF'),
                        'timestamp': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Timestamp')
                    }
                )
            ),
            400: openapi.Response(description="Invalid request"),
            503: openapi.Response(description="Blynk service unavailable")
        }
    )
    def post(self, request):
        """
        Set pump status on Blynk
        """
        status = request.data.get('status')
        
        if status is None:
            return Response(
                {"error": "Missing 'status' field"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Convert to 1 or 0 for Blynk
        value = 1 if status else 0
        
        success = BlynkIntegration.set_pin_value("V2", value)
        
        if success:
            from datetime import datetime
            return Response({
                'success': True,
                'pump_status': value,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return Response(
                {"error": "Failed to update pump status on Blynk"}, 
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


class BlynkDashboardDataView(APIView):
    """
    API endpoint to get all sensor data from Blynk for dashboard display
    """
    @swagger_auto_schema(
        tags=['api/blynk/dashboard-data/'],
        operation_id='blynk_dashboard_data',
        operation_summary="Get All Sensor Data from Blynk",
        operation_description="Gets all sensor data from Blynk IoT platform for dashboard display",
        responses={
            200: openapi.Response(
                description="Dashboard data retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'temperature': openapi.Schema(type=openapi.TYPE_NUMBER, description='Temperature value from Blynk'),
                        'soil_moisture': openapi.Schema(type=openapi.TYPE_NUMBER, description='Soil moisture value from Blynk'),
                        'pump_status': openapi.Schema(type=openapi.TYPE_INTEGER, description='Pump status: 1=ON, 0=OFF'),
                        'is_pump_on': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Is pump running'),
                        'timestamp': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Timestamp')
                    }
                )
            ),
            503: openapi.Response(description="Blynk service unavailable")
        }
    )
    def get(self, request):
        """
        Get all data from Blynk for dashboard display
        """
        temp = BlynkIntegration.get_pin_value("V0")
        soil = BlynkIntegration.get_pin_value("V1")
        pump = BlynkIntegration.get_pin_value("V2")
        
        if temp is not None and soil is not None and pump is not None:
            from datetime import datetime
            pump_value = int(pump) if pump is not None else None
            return Response({
                'temperature': float(temp) if temp is not None else None,
                'soil_moisture': float(soil) if soil is not None else None,
                'pump_status': pump_value,
                'is_pump_on': bool(pump_value) if pump_value is not None else None,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return Response(
                {"error": "Failed to retrieve data from Blynk"}, 
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )