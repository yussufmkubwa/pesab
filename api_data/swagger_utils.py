from drf_yasg.inspectors import SwaggerAutoSchema

class CustomSwaggerAutoSchema(SwaggerAutoSchema):
    """
    Custom Swagger schema class that organizes API endpoints into three main headers:
    1. Authentication API
    2. User Management API
    3. IoT Device API
    """
    def get_tags(self, *args, **kwargs):
        tags = super().get_tags(*args, **kwargs)
        
        if not tags:
            return tags
            
        primary_tag = tags[0]
        
        # Map endpoints to their respective header groups
        if primary_tag.startswith('api/auth/'):
            return ["1-Authentication API"]
        elif primary_tag.startswith('api/users/'):
            return ["2-User Management API"]
        elif primary_tag.startswith('api/iot/'):
            return ["3-IoT Device API"]
        elif primary_tag.startswith('api/devices/'):
            return ["4-Web Interface Device API"]
        else:
            return ["5-Other Endpoints"]