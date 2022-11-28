from .models import ( GHO_IndicatorFacts,FactsGHO_IndicatorsViewMapped,)
from rest_framework.serializers import (ModelSerializer, ReadOnlyField)

class FactGHODataIndicatorSerializer(ModelSerializer):
    class Meta:
        model = FactsGHO_IndicatorsViewMapped
        fields = [
            'indicator', 'location','categoryoption','datasource',
            'measuremethod','numerator_value','denominator_value',
            'value_received','min_value','max_value','target_value',
            'string_value','start_period', 'end_period','period',
            'status',
            ] 