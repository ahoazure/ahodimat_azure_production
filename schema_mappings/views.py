from django.shortcuts import render
from django.db import IntegrityError
from sqlite3 import IntegrityError
from requests.exceptions import ConnectionError
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status,generics,viewsets #for generating api parameters

import http.client
import urllib3
import requests
import re # import regular expression to stripoff http scheme from mediators url
import json
import http.client
import base64
import datetime
from datetime import date
from datetime import datetime
from dateutil import rrule # important in returning monthly periods
from dateutil.relativedelta import relativedelta

from openhim_mediator_utils.main import Main
from time import sleep

import os # necessary for accessing filesystem from current project
import MySQLdb # drivers for accessing the database exceptions
import dotenv # necessary for reading .env config files in .config

from dctmetadata.models import (DCTIndicators,DCTLocations,
   DCT_Categoryoptions,DCT_Datasource,DCT_Measuretype)

from dhis2metadata.models import (DHIS2Indicators, 
    PeriodType,DHIS2_URLEndpointPathMapped)

from .models import (FactsDHIS2_Indicators,FactsDHIS2_IndicatorsMapped,
	FactsDHIS2_QueryParametersMapped,DHIS2DCT_LocationsMapped,
	DHIS2_QueryParameters)

from .serializers import (FactDataIndicatorSerializer,
	DHIS2QueryParametersViewSerializer)
from dctmetadata.models import (DCT_URLEndpointPathMapped,)
from authentication.models import MediatorConfigs # import server settings
from utilities import security # used to encrypt sensitive passwords


# Import .env variables before assiging the values to the BASE_URL in home directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_file = os.path.join(BASE_DIR, ".conf/.env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)


class FactDataIndicatorViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = FactsDHIS2_IndicatorsMapped.objects.all()
    serializer_class = FactDataIndicatorSerializer
    
    def get_dhis_indicatorfacts(self):
        payload = None
        params = DHIS2_URLEndpointPathMapped.objects.values(
            'id','url','username','password','endpoint','status').get(
                status=1) 

        password = security.decrypt(params['password']) # decode password    
        authvars = params['username']+":"+ password #create credentials
        
        encodedBytes = base64.b64encode(authvars.encode("utf-8"))
        encodedStr = str(encodedBytes, "utf-8")
        auth_dhis2 = "Basic " + encodedStr
             
        headers = { # modified headers to pass tenant header specific to MIFOS
            'Authorization': auth_dhis2,
            'Accept': "application/json",
            } 

        try:
            dhisurl = params['url']
            location_param = DHIS2DCT_LocationsMapped.objects.values(
                'id','dhis_uid','location_name').get(locationlevel=2) # get mapped DHIS2 mapped locations 
            location=location_param['dhis_uid'] # catch index out of range exception            
        
            params = FactsDHIS2_QueryParametersMapped.objects.values(
                'pt','dx','ou','dct_indicator','periodname',
                'startDate','endDate').get(status=1) 
        
            param_id=params['pt']# Considered when determining DHIS2 endpoint to consume	
            param_dx=params['dx']# Considered when adding indicator uid to the endpoint
            param_ou=params['ou']# Considered when adding orgunit to the endpoint
            indicator_id=params['dct_indicator']# Considered when adding orgunit to the endpoint

            param_start=params['startDate']# Considered when adding start date query parameter
            param_end=params['endDate']# Considered when adding end date query parameter

            location_queryset = DHIS2DCT_LocationsMapped.objects.values('id').get(
            dhis_uid=param_ou)
            location_id=location_queryset['id']

            annaul_list= [y for y in range(params['startDate'].year,params['endDate'].year + 1)]
            string_years = [str(int) for int in annaul_list] #Convert each integer to a string
            yearsrange = ";".join(string_years) # convert period list to semicolon-seperated string
            
            months_list=[]
            for dt in rrule.rrule(rrule.MONTHLY, dtstart=param_start, until=param_end):
                months_list.append(dt.strftime("%Y%m")) 
                monthsrange = ";".join(months_list) # create semicolon-seperated list of monthly periods
            if param_id == 1:
                dhisurl = dhisurl+'/analytics.json?dimension=dx:{dx}&dimension=ou:{ou}'.format_map(
                    params)+"&dimension=pe:"+yearsrange+"&includeNumDen=true" # get data using fixed annual periods	                       
            elif param_id == 2 or param_id==3:
                dhisurl = dhisurl+'/analytics.json?dimension=dx:{dx}&dimension=ou:{ou}'.format_map(
                    params)+"&dimension=pe:"+monthsrange+"&includeNumDen=true" # get data using fixed annual periods	                                     
            elif param_id >= 4 and param_id <=7:
                dhisurl = dhisurl+'/analytics.json?dimension=dx:{dx}&dimension=ou:{ou}&dimension=pe:{periodname}&includeNumDen=true'.format_map(
                    params)# to be formatted tp accept uids and dimensions consider the id ad params	
            else:
                dhisurl = dhisurl+'/analytics.json?dimension=dx:{dx}&dimension=ou:{ou}'.format_map(
                    params)+"&dimension=pe:"+yearsrange+"&includeNumDen=true" # rawData endpoint allows retrieval of data using fixed periods	                      
                        
            response = requests.request("GET", dhisurl, data=payload, headers=headers,) #by-pass Cert verificartion
            payload = json.loads(response.text) # extract the payload part of the response
            
            self.save_dhis2_indicatorfacts(payload,indicator_id,location_id,params) # call the save method
    
        except (MySQLdb.IntegrityError, MySQLdb.OperationalError,MySQLdb.IntegrityError,
            IndexError,ValueError) as e: 
            pass       
        return Response(payload)	               		   
   

    """
	 This functions must receive self in order to save data extracted from DHIS2
    """
    def save_dhis2_indicatorfacts(self,data,indicator_id,location_id,params): 
        rows = data['rows']	
        pt = params['pt'] # get period type id from params for use in if-else date conversion
        if rows:
            for item in rows:
                try: # start by genetating a date object from DHIS2 periods using strptime()
                    if pt==1 or pt==4 or pt==5:
                        start_date = datetime.strptime(item[2], "%Y").date() # get year start date
                        end_date = start_date+relativedelta(months=12, days=-1) # get year end date
                    else:
                        start_date = datetime.strptime(item[2], "%Y%m").date() # get month start date
                        end_date = start_date+relativedelta(months=1, days=-1) # get month end date

                    if not FactsDHIS2_Indicators.objects.filter(indicator=indicator_id,
                        location=location_id,period=int(item[2])).exists():
                        FactsDHIS2_Indicators.objects.update_or_create(
                            indicator=DCTIndicators.objects.get(
                                pk=indicator_id), # Must be an instance of DCTIndicators,
                            location=DCTLocations.objects.get(
                                pk=location_id),
                            categoryoption =DCT_Categoryoptions.objects.get(
                                pk=9),# default value which must be mapped on admin interface
                            datasource =DCT_Datasource.objects.get(
                                pk=2),# default value which must be mapped on admin interface
                            measuremethod=DCT_Measuretype.objects.get(
                                pk=1),# default value which must be mapped on admin interface
                            start_period=start_date,
                            end_period=end_date,
                            period=item[2],
                            value_received=item[3],
                            numerator_value=item[4],
                            denominator_value=item[5],
                        )
                except (MySQLdb.IntegrityError, MySQLdb.OperationalError,MySQLdb.IntegrityError,
                    IndexError,ValueError): 
                    pass # ignore duplicates,index out of range and missing values


    def post_dctfact_indicators(self):
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
        mediatorurl = mediurl['mediator_url']+"/api/data/facts-indicators/"
               
        if mediatorurl:
            try:
              response = requests.request("GET", mediatorurl)
              payload = json.loads(response.text)
              
            #   import pdb; pdb.set_trace()	
              data=self.mediators_post_factindicators(dct_dataurl,payload,headers) 
              print(data) 
            #   import pdb; pdb.set_trace()	
       
              return Response(payload)                  
            except (MySQLdb.IntegrityError, MySQLdb.OperationalError,MySQLdb.IntegrityError,
                IndexError,ValueError):
               pass
        return Response(payload)	

    """
    This method receives data from the mediator URL fact table-view and transforms the array of
	dictionaries from MariaDB database into a JSON format required by the requests.POST method. 
	The FOR loop then sends each object dictionary as a record in DCT facts_data_indicator table. 
    """
    def mediators_post_factindicators(self,dct_dataurl,facts,headers):
        payload = None # initialize post payload

        for items in facts:
            # import pdb; pdb.set_trace()	

            if items['status']=='approved':
                response = requests.post(dct_dataurl,data=items,headers=headers)
                payload = response.text
                print(payload)
        return payload


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
        # import pdb; pdb.set_trace()	
          
        if mediatorurl:
            try:
              response = requests.request("GET", mediatorurl)
              payload = json.loads(response.text)
              
            #   import pdb; pdb.set_trace()	

              data=self.mediators_post_gho_indicator_facts(dct_dataurl,payload,headers)         
              return Response(payload)                  
            except (MySQLdb.IntegrityError, MySQLdb.OperationalError,MySQLdb.IntegrityError,
                IndexError,ValueError):
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
            if items['status']=='approved': # NB: facts in DIMAT must be approved before exporting to DCT 
                response = requests.post(dct_dataurl,data=items,headers=headers)
                payload = response.text
                print(payload)
        return payload
