from .models import (GHO_URLEndpointPathMapped,)
from rest_framework.serializers import (ModelSerializer,)

class GHO_URLEndpointPathMappedSerializer(ModelSerializer):
    class Meta:
        model = GHO_URLEndpointPathMapped
        fields = '__all__'
