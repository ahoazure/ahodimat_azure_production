from .models import (FactsDHIS2_IndicatorsMapped,DHIS2_QueryParameters,
    FactsDHIS2_QueryParametersMapped,)
from rest_framework.serializers import (ModelSerializer, ReadOnlyField)

class FactDataIndicatorSerializer(ModelSerializer):
    class Meta:
        model = FactsDHIS2_IndicatorsMapped
        fields = [
            'indicator', 'location','categoryoption','datasource',
            'measuremethod','numerator_value','denominator_value',
            'value_received','min_value','max_value','target_value',
            'string_value','start_period', 'end_period','period',
            'status',
            ] 


class DHIS2QueryParametersSerializer(ModelSerializer):
    class Meta:
        model = DHIS2_QueryParameters
        fields = [
            'id','indicator','location','start_period',
            'end_period','period','status',] 


class DHIS2QueryParametersViewSerializer(ModelSerializer):
    class Meta:
        model = FactsDHIS2_QueryParametersMapped
        fields = [
            'id','dx','ou','startDate','endDate','period',
            'periodname','status' ] 