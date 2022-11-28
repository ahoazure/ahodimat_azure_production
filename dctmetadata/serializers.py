from .models import (DCT_URLEndpointPathMapped,)
from rest_framework.serializers import (ModelSerializer,)

class DCT_URLEndpointPathMappedSerializer(ModelSerializer):
    class Meta:
        model = DCT_URLEndpointPathMapped
        fields = '__all__'
