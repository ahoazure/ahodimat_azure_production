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
from . models import (DCTIndicators,DCTLocations,DCT_URLEndpointPath,
        DCT_URLEndpointPathMapped,DCT_Categoryoptions,DCT_Datasource,
        DCT_Measuretype) # add DCTConfigs
from . serializers import (DCT_URLEndpointPathMappedSerializer,)
from authentication.models import MediatorConfigs # import server settings


class DCTAPIPathManagementView(viewsets.ReadOnlyModelViewSet):
    serializer_class = DCT_URLEndpointPathMappedSerializer
 
    def get_queryset(self):
        try:
            qs = DCT_URLEndpointPathMapped.objects.filter(status=1) 
            return qs
        except (MySQLdb.IntegrityError, MySQLdb.OperationalError,):
            pass

class DCTMetadataManagementView(APIView):

    def get(self, request,format=None):
        payload = None

        params = DCT_URLEndpointPathMapped.objects.values(
            'id','url','username','password','endpoint','status').get(
                status=1)
        
        password = security.decrypt(params['password'])    
        authvars = params['username']+":"+password
        
        # Encode DHIS2 user credentials using Base64 Encoding scheme
        encodedBytes = base64.b64encode(authvars.encode("utf-8"))
        encodedStr = str(encodedBytes, "utf-8")
        auth_dct = "Basic " + encodedStr
        headers = { # modified headers to pass tenant header specific to MIFOS
            'Authorization': auth_dct,
            'Accept': "application/json",
            } 
        
        try:  
            if params['id'] == 1 or 'indicators' in params['endpoint']: 
                dcturl = params['url']+params['endpoint']
            elif params['id'] == 2 or 'locations' in params['endpoint']:
                dcturl = params['url']+params['endpoint']
            response = requests.request("GET",dcturl,data=payload,headers=headers)	
            # import pdb; pdb.set_trace()	
            payload = json.loads(response.text) # extract the payload part of the response 
        
        except(IndexError,ValueError,requests.exceptions.RequestException,TypeError,
            MySQLdb.IntegrityError, MySQLdb.OperationalError,JSONDecodeError,):
            pass
        return Response(payload)   


    def _dct_save_metadata(self):
        payload = None
        params = DCT_URLEndpointPathMapped.objects.values(
            'id','url','username','password','endpoint','status').get(
                status=1)
        
        password = security.decrypt(params['password'])    
        authvars = params['username']+":"+password
        
        # import pdb; pdb.set_trace()	

        
        # Encode DHIS2 user credentials using Base64 Encoding scheme
        encodedBytes = base64.b64encode(authvars.encode("utf-8"))
        encodedStr = str(encodedBytes, "utf-8")
        auth_dct = "Basic " + encodedStr
        
        headers = { # modified headers to pass tenant header specific to MIFOS
            'Authorization': auth_dct,
            'Accept': "application/json",
            } 

        try:  
            if 'indicators' in params['endpoint']: # removed logical expression to work with in operator
                dcturl = params['url']+params['endpoint']
                response = requests.request("GET",dcturl,data=payload,headers=headers)
                payload = json.loads(response.text)
                
                for child in payload['results']: #iterate to display all objects in the json array
                    indicator = DCTIndicators.objects.update_or_create(
                        id = int(child['afrocode'][3:]),					
                        code = child['afrocode'],	
                        name = child['translations']['en']['name'],) 
         
            elif 'locations' in params['endpoint']:
                dcturl = params['url']+params['endpoint']
                response = requests.request("GET",dcturl,data=payload,headers=headers)
                payload = json.loads(response.text)
                
                for child in payload['results']: #iterate to display objects in the array
                    location = DCTLocations.objects.update_or_create(
                    id = child['location_id'],				
                    location_id = child['location_id'],					
                    code = child['code'],
                    name = child['name'],
                    locationlevel = child['locationlevel'],)
                    

            elif 'disagregation' in params['endpoint']: # removed logical expression to work with in operator
                dcturl = params['url']+params['endpoint']
                response = requests.request("GET",dcturl,data=payload,headers=headers)
                payload = json.loads(response.text)
            
                for child in payload['results']: #iterate to display all objects in the json array
                    categoryoptions = DCT_Categoryoptions.objects.update_or_create(
                        id = int(child['code'][3:]),
                        category = child['category'],						
                        code = child['code'],	
                        name = child['name'],
                        description= child['description'],
                    ) 
            elif 'sources' in params['endpoint']: # removed logical expression to work with in operator
                dcturl = params['url']+params['endpoint']
                response = requests.request("GET",dcturl,data=payload,headers=headers)
                payload = json.loads(response.text)
                
                # import pdb; pdb.set_trace()	

                for child in payload['results']: #iterate to display all objects in the json array
                    categoryoptions = DCT_Datasource.objects.update_or_create(
                        id = int(child['code'][3:]),
                        code = child['code'],	
                        name = child['name'],
                        description= child['description'],
                    ) 
            elif 'measure' in params['endpoint']: # removed logical expression to work with in operator
                dcturl = params['url']+params['endpoint']
                response = requests.request("GET",dcturl,data=payload,headers=headers)
                payload = json.loads(response.text)
                
                # import pdb; pdb.set_trace()	

                for child in payload['results']: #iterate to display all objects in the json array
                    categoryoptions = DCT_Measuretype.objects.update_or_create(
                        id = int(child['code'][3:]),
                        code = child['code'],	
                        name = child['name'],
                        description= child['description'],
                    ) 
                    # import pdb; pdb.set_trace()	

        except(IndexError,ValueError,requests.exceptions.RequestException,JSONDecodeError,
            TypeError,MySQLdb.OperationalError,MySQLdb.IntegrityError):
            pass
        return payload

    def mediators_dct_metadata(self): 
        metadata= self._dct_save_metadata() 
        return metadata 
