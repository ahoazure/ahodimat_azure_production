from .models import (DHIS2_URLEndpointPathMapped,)
from rest_framework.serializers import (ModelSerializer,)

class DHIS2_URLEndpointPathMappedSerializer(ModelSerializer):
    class Meta:
        model = DHIS2_URLEndpointPathMapped
        fields = '__all__'
