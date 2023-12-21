from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from dateutil.relativedelta import * 
from datetime import timedelta
import datetime

from authentication.models import CustomUser


class GHOMainConfigs(models.Model):   
    CHOICES=((1,"Active"),(0,"Innactive"))
    url_regex = RegexValidator(
        regex=r'https?:\/\/(?:w{1,3}\.)?[^\s.]+(?:\.[a-z]+)*(?::\d+)?(?![^<]*(?:<\/\w+>|\/?>))',
        message="Valid URL:'https://abc.com; or http://abc.com:8000'")

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, models.PROTECT, blank=True,
        null=True,verbose_name='GHO User/Email')         
    gho_url = models.CharField(max_length=200,validators=[url_regex],
        verbose_name='GHO Base URL') #base url
    gho_user = models.CharField(max_length=200,blank=True,null=True,
        verbose_name='Username') #auth user
    gho_passkey = models.CharField(max_length=300,blank=True,null=True,
        verbose_name='Password') #auth pass
    status = models.BooleanField(choices=CHOICES,verbose_name='Status',
        default=CHOICES[0][0])
    
    class Meta:
        managed = True
        db_table = 'gho_main_configs'
        verbose_name = 'GHO Setup'
        verbose_name_plural = ' GHO Settings'
        
    def __str__(self):
        return "%s" %(self.gho_url)
    

    def clean(self):
        if (self.gho_url.endswith('/')):
            raise ValidationError({'dhis2_url':_(
                'Invalid Base URL. A valid GHO Base URL should NOT have a \
                    forward slash (/) at the end!')}) 


class GHOSpatialDimensionCountries(models.Model):
    id = models.AutoField(primary_key=True,)     
    code = models.CharField(max_length=45,verbose_name ='Country Code',
        default=None)
    name = models.CharField(max_length=255,verbose_name ='Country Name',
        default=None)
    dimension = models.CharField(max_length=45,blank=True,null=True,
         verbose_name ='Dimension Type')
    parent = models.CharField(max_length=45,blank=True,null=True,
         verbose_name ='Parent Dimension')

    class Meta:
        managed = True
        db_table = 'gho_afro_countries'
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        ordering = ('name',)

    def __str__(self):
        return self.name


class GHOIndicators(models.Model):
    id = models.AutoField(primary_key=True,)  
    code = models.CharField(max_length=45,verbose_name ='Indicator Code',
        default=None)
    name = models.CharField(max_length=255,verbose_name ='Indicator Name',
        default=None)
    language = models.CharField(max_length=100,blank=True,null=True,
         verbose_name ='Language')
    reference = models.CharField(max_length=100,blank=True, null=True, 
        verbose_name ='Indicator Reference',default ='GHO',)

    class Meta:
        managed = True
        db_table = 'gho_indicators'
        verbose_name = 'GHO Indicator'
        verbose_name_plural = 'GHO Indicators'
        ordering = ('name',)
    
    def __str__(self):
        return self.name


class GHO_URLEndpointPath(models.Model):
    CHOICES=((1,"Active"),(0,"Innactive"))
    id = models.AutoField(primary_key=True)   
    url = models.ForeignKey(GHOMainConfigs, models.CASCADE,
        verbose_name = 'GHO Base URL')
    api_endpoint = models.CharField(verbose_name='Resource API Endpoint',
        max_length=250,blank=True,null=False)
    status = models.BooleanField(choices=CHOICES,blank=False,
        verbose_name='Status',)
    date_created = models.DateTimeField(blank=True, null=True, 
        auto_now_add=True,verbose_name = 'Date Created')
    date_lastupdated = models.DateTimeField(blank=True, 
        null=True,auto_now=True,
        verbose_name = 'Date Modified')

    class Meta:
        managed = True
        db_table = 'gho_api_endpoint'
        verbose_name = ' Map API'
        verbose_name_plural = 'Map APIs'
        ordering = ('url',)

    def __str__(self):
         return str(self.url)


    def clean(self):
        if not (self.api_endpoint.startswith('/')):
            raise ValidationError({'api_endpoint':_(
                'Invalid API Endpoint! A valid endpoint must start with a forward slash (/)')})    

        if self.status:
            active = GHO_URLEndpointPath.objects.filter(status=1)
            if self.pk:
                active = active.exclude(pk=self.pk)
            if active.exists():
                raise ValidationError("Only one record can be active at a time")



class GHO_URLEndpointPathMapped(models.Model):
    id = models.AutoField(primary_key=True,verbose_name ='Path ID',)
    url = models.CharField(max_length=45,verbose_name ='GHO Base URL',)
    endpoint = models.CharField(max_length=100,verbose_name ='Resource Path')
    username = models.CharField(max_length=45,)
    password = models.CharField(max_length=300,) 
    resource_endpoint = models.CharField(
        max_length=2083,verbose_name ='Resource URL Endpoint')     
    status = models.PositiveSmallIntegerField(blank=True,null=False,
        verbose_name ='Status',default=0)     

    class Meta:
        managed = False
        db_table = 'vw_gho_mapped_api_endpoint'
        verbose_name = 'Mapped GHO API'
        verbose_name_plural = 'Mapped GHO API'
        ordering = ('url',)