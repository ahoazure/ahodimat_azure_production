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

import re # import regular expression to strip off https in mediators host

from datetime import date,datetime
from openhim_mediator_utils.main import Main
from time import sleep
import json
import http.client
import base64

import os # necessary for accessing filesystem from current project
# import dotenv # necessary for reading .env config files in .config
from .models import (DHIS2Indicators,OrganizationUnits,PeriodType,
    DHIS2_URLEndpointPath,DHIS2_URLEndpointPathMapped)# add DHIS2Configs
from .serializers import (DHIS2_URLEndpointPathMappedSerializer,)
from authentication.models import MediatorConfigs # import server settings
from utilities import security # used to encrypt sensitive passwords


class DHIS2APIPathManagementView(viewsets.ReadOnlyModelViewSet):
    serializer_class = DHIS2_URLEndpointPathMappedSerializer
 
    def get_queryset(self):
        qs = DHIS2_URLEndpointPathMapped.objects.filter(status=1) 
        return qs


class DHIS2MetadataManagementView(APIView):

    def get(self, request,format=None):
        payload = None
        params = DHIS2_URLEndpointPathMapped.objects.values(
            'id','url','username','password','endpoint','status').get(
                status=1)

        password = security.decrypt(params['password'])  
        authvars = params['username']+":"+ password

        # Encode DHIS2 user credentials using Base64 Encoding scheme
        encodedBytes = base64.b64encode(authvars.encode("utf-8"))
        encodedStr = str(encodedBytes, "utf-8")
        auth_dhis2 = "Basic " + encodedStr
        headers = { # modified headers to pass tenant header specific to MIFOS
            'Authorization': auth_dhis2,
            'Accept': "application/json",
            } 
        
        try:  
            if 'organisationUnits' in params['endpoint']: 
                dhisurl = params['url']+params['endpoint']
            elif 'indicators' in params['endpoint']:
                dhisurl = params['url']+params['endpoint']
            response = requests.request("GET",dhisurl,data=payload,headers=headers)	
            # import pdb; pdb.set_trace()	
            payload = json.loads(response.text) # extract the payload part of the response 
        
        except(IndexError,ValueError,requests.exceptions.RequestException,
        JSONDecodeError,TypeError):
            pass
        return Response(payload)    

 
    def _get_dhis2_indicators(self):
        payload = None    
        try:
            params = MediatorConfigs.objects.values(
                'id','mediator_url','mediator_port','status').get(
                status=1)            
            mediatorurl = params['mediator_url']+"/api/dhis/indicators/?=&limit=300"
            response = requests.request("GET", mediatorurl)
            if response.status_code==200:
                payload = json.loads(response.text)                      
        except (requests.exceptions.RequestException,JSONDecodeError,
            TypeError) as e:
            pass
        return payload


    def mediators_save_indicators(self):
        dhis2_data = self._get_dhis2_indicators()
        if dhis2_data:
            for child in dhis2_data['indicators']: #iterate to display all objects in the json array
                indicators = DHIS2Indicators.objects.update_or_create(
                uid = child['id'],					
                # code = child['code'],	
                name = child['name'],)
            return indicators


    def _dhis_save_metadata(self):
        payload = None
        params = DHIS2_URLEndpointPathMapped.objects.values(
            'id','url','username','password','endpoint','status').get(
                status=1)
        if params['username'] and params['password']:
            password = security.decrypt(params['password']) 
            authvars = params['username']+":"+ password
        
            # Encode DHIS2 user credentials using Base64 Encoding scheme
            encodedBytes = base64.b64encode(authvars.encode("utf-8"))
            encodedStr = str(encodedBytes, "utf-8")
            auth_dhis2 = "Basic " + encodedStr
            headers = { # modified headers to pass tenant header specific to MIFOS
                'Authorization': auth_dhis2,
                'Accept': "application/json",
                }
        else:
            print ('Password is required')
        
        try:  
            if 'organisationUnits' in params['endpoint']: 
                dhisurl = params['url']+params['endpoint']
                response = requests.request("GET",dhisurl,data=payload,headers=headers)
                payload = json.loads(response.text)               
                
                # import pdb; pdb.set_trace()	

                for child in payload['organisationUnits']: #iterate to display all objects in the json array
                    # import pdb; pdb.set_trace()	
                    organization = OrganizationUnits.objects.update_or_create(
                        uid = child['id'],					
                        code = child['code'],
                        name = child['name'],
                    )       
            elif 'indicators' in params['endpoint']:
                dhisurl = params['url']+params['endpoint']
                response = requests.request("GET",dhisurl,data=payload,headers=headers)
                payload = json.loads(response.text)
                
                for child in payload['indicators']: #iterate to display all objects in the json array
                    indicators = DHIS2Indicators.objects.update_or_create(
                        uid = child['id'],					
                        # code = child['code'],	
                        name = child['name'],
                    )
        except(IndexError,ValueError,requests.exceptions.RequestException,
        JSONDecodeError,TypeError):
            pass
        return payload


    def mediators_dhis_metadata(self): 
        metadata= self._dhis_save_metadata() 
        return metadata 



