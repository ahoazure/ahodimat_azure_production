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
from openhim_mediator_utils.main import Main
from time import sleep
import json
import http.client
import base64

import os # for accessing filesystem from current project
import MySQLdb # drivers for accessing the database exceptions

# import dotenv # necessary for reading .env config files in .config
from .models import (GHOIndicators,GHOSpatialDimensionCountries,
    GHO_URLEndpointPath,GHO_URLEndpointPathMapped,GHOMainConfigs)
from . serializers import (GHO_URLEndpointPathMappedSerializer,)
from authentication.models import MediatorConfigs # import server settings


class DCTAPIPathManagementView(viewsets.ReadOnlyModelViewSet):
    serializer_class = GHO_URLEndpointPathMappedSerializer
 
    def get_queryset(self):
        try:
            qs = GHO_URLEndpointPathMapped.objects.filter(status=1) 
            return qs
        except (MySQLdb.IntegrityError, MySQLdb.OperationalError,):
            pass

class GHOMetadataManagementView(APIView):
    def get(self, request,format=None):
        payload = None
        params = GHO_URLEndpointPathMapped.objects.values(
            'id','url','username','password','endpoint','status').get(
                status=1)
        username = params['username']
        password = params['password']
        
        if username or password:
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
            if params['id'] == 1 or 'COUNTRY' in params['endpoint']: 
                ghoapiurl = params['url']+params['endpoint']
            elif params['id'] == 2 or 'Indicator' in params['endpoint']:
                ghoapiurl = params['url']+params['endpoint']
            response = requests.request("GET",ghoapiurl,data=payload,headers=headers)	
            # import pdb; pdb.set_trace()	
            payload = json.loads(response.text) # extract the payload part of the response 
        
        except(IndexError,ValueError,requests.exceptions.RequestException,TypeError,
            JSONDecodeError,MySQLdb.IntegrityError, MySQLdb.OperationalError):
            pass
        return Response(payload)   


    def _gho_save_metadata(self):
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
            if 'COUNTRY' in params['endpoint']: 
                ghoapiurl = params['url']+params['endpoint']
                response = requests.request("GET",ghoapiurl,data=payload,headers=headers)
                payload = json.loads(response.text)
                
                for child in payload['value']: #iterate to display objects in the array
                    country = GHOSpatialDimensionCountries.objects.update_or_create(
                    code = child['Code'],
                    name = child['Title'],
                    dimension = 'Country',
                    parent = child['ParentTitle'],)

            elif 'Indicator' in params['endpoint']:
                ghoapiurl = params['url']+params['endpoint']
                response = requests.request("GET",ghoapiurl,data=payload,headers=headers)
                payload = json.loads(response.text)
                for child in payload['value']: #iterate to display all objects in the json array
                    indicator = GHOIndicators.objects.update_or_create(
                        code = child['IndicatorCode'],	
                        name = child['IndicatorName'],
                        language = child['Language'],
                    ) 

        except(IndexError,ValueError,requests.exceptions.RequestException,TypeError,
            JSONDecodeError,MySQLdb.IntegrityError, MySQLdb.OperationalError):
            pass
        return payload

    def mediators_gho_metadata(self): 
        metadata= self._gho_save_metadata() 
        return metadata 
