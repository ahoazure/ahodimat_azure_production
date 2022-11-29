from django.shortcuts import render

from django.http import HttpResponse
from django.forms.models import model_to_dict
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import viewsets #for generating api parameters
from rest_framework.response import Response
from rest_framework import status

import urllib3
import requests
from requests.exceptions import ConnectionError
from json.decoder import JSONDecodeError
from utilities import security # used to encrypt sensitive passwords


import re # import regular expression to strip off https in mediators host

from datetime import date,datetime
from time import sleep
import json
import http.client
import base64

import os # necessary for accessing filesystem from current project
import MySQLdb # drivers for accessing the database exceptions

from dctmetadata.models import (DCT_URLEndpointPathMapped,)
from ghometadata.models import (GHOIndicators,GHOSpatialDimensionCountries,
    GHO_URLEndpointPath,GHO_URLEndpointPathMapped,GHOAPIConfigs)

from .models import GHO_IndicatorFacts,FactsGHO_IndicatorsViewMapped
from authentication.models import MediatorConfigs # import server settings
from .serializers import (FactGHODataIndicatorSerializer,)

class FactGHODataIndicatorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FactsGHO_IndicatorsViewMapped.objects.all()
    serializer_class = FactGHODataIndicatorSerializer

    def post_ghofact_indicators(self):
        payload = None # initialize DCT payload
        params = DCT_URLEndpointPathMapped.objects.values(
            'id','url','username','password','endpoint','status').get(
                status=1)

        dct_dataurl = params['url']+"/api/indicator_data/" # get DCT facts urls

        password = security.decrypt(params['password']) # decode password 
        authvars = params['username']+":"+ password #create credentials
               
        encodedBytes = base64.b64encode(authvars.encode("utf-8"))
        encodedStr = str(encodedBytes, "utf-8")
        auth_dct = "Basic " + encodedStr

        headers = { # modified headers to pass tenant header specific to MIFOS
            'Authorization': auth_dct,
            'Accept': "application/json",
            } 
        
        mediurl = MediatorConfigs.objects.values('mediator_url',
            'mediator_port','status').get(status=1)     
        mediatorurl = mediurl['mediator_url']+"/api/data/gho-facts/"          
        if mediatorurl:
            try:
              response = requests.request("GET", mediatorurl)
              payload = json.loads(response.text)
              data=self.mediators_post_gho_indicator_facts(dct_dataurl,payload,headers)         
              return Response(payload)                  
            except (MySQLdb.IntegrityError,MySQLdb.OperationalError,IndexError,ValueError):
               pass
        return Response(payload)	


    """
    This method receives data from the mediator URL fact table-view and transforms the array of
	dictionaries from MariaDB database into a JSON format required by the requests.POST method. 
	The FOR loop then sends each object dictionary as a record in DCT facts_data_indicator table. 
    """
    def mediators_post_gho_indicator_facts(self,dct_dataurl,facts,headers):
        payload = None # initialize post payload
        for items in facts:
            if items['status']=='approved':
                response = requests.post(dct_dataurl,data=items,headers=headers)
                payload = response.text
                # print(payload)
        return payload



class GHOIndicatiorFactsManagementView(APIView):

    def _gho_save_datasets(self):
        payload = None
        params = GHO_URLEndpointPathMapped.objects.values(
            'id','url','username','password','endpoint','status').get(
                status=1)
        username = params['username']
        password = params['password']
        
        if username or password: # checks whether the username and password are empty
            password = security.decrypt(password)
            authvars = username+":"+password
            encodedBytes = base64.b64encode(authvars.encode("utf-8"))
            encodedStr = str(encodedBytes, "utf-8")
            auth_ghoapi = "Basic " + encodedStr
            headers = { # modified headers to pass tenant header specific to MIFOS
            'Authorization': auth_ghoapi,
            'Accept': "application/json",
            } 
        else:
            headers = { # modified headers to pass tenant header specific to MIFOS
            'Accept': "application/json",
            } 

        try:  
            if 'IndicatorCode' in params['endpoint']: 
                ghoapiurl = params['url']+params['endpoint']
                response = requests.request(
                    "GET",ghoapiurl,data=payload,headers=headers)
                payload = json.loads(response.text)
                          
                for child in payload['value']:
                    GHO_IndicatorFacts.objects.update_or_create(
                        indicator = child['IndicatorCode'],
                        location = child['SpatialDim'],
                        category = child['Dim1Type'],                   
                        categoryoption = child['Dim1'],
                        numeric_value = child['NumericValue'],
                        adjusted_value = child['Value'],                   
                        min_value = child['High'],
                        max_value = child['Low'],                    
                        period_type = child['TimeDimType'],                    
                        start_period= child['TimeDimensionBegin'].split('T')[0],  
                        end_period= child['TimeDimensionEnd'].split('T')[0],                      
                        period = child['TimeDim'],                                    
                    )
        except(IndexError,ValueError,requests.exceptions.RequestException,JSONDecodeError,
            TypeError,MySQLdb.OperationalError,MySQLdb.IntegrityError):
            pass
        return payload

    def mediators_gho_save_dataset(self):
        dataset= self._gho_save_datasets() 
        return dataset 