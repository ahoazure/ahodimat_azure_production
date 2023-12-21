from django.db import models

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from datetime import timedelta
import datetime

from authentication.models import CustomUser
# from mainconfigs.models import DHIS2UserLocation


class WBGMainConfigs(models.Model):   
    CHOICES=((1,"Active"),(0,"Innactive"))
    url_regex = RegexValidator(
        regex=r'https?:\/\/(?:w{1,3}\.)?[^\s.]+(?:\.[a-z]+)*(?::\d+)?(?![^<]*(?:<\/\w+>|\/?>))',
        message="Valid URL:'https://abc.com; or http://abc.com:8000'")

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, models.PROTECT, blank=True,
        null=True,verbose_name='GHO User/Email')         
    wbapi_url = models.CharField(max_length=200,validators=[url_regex],
         blank=False, null=False,verbose_name='World Bank API Base URL') #base url
    wbapi_user = models.CharField(max_length=200,blank=True,null=True,
        verbose_name='Username') #auth user
    wbapi_passkey = models.CharField(max_length=300,blank=True,null=True,
        verbose_name='Password') #auth pass
    status = models.BooleanField(choices=CHOICES,verbose_name='Status',
        default=CHOICES[0][0])
    
    class Meta:
        managed = True
        db_table = 'worldbank_main_configs'
        verbose_name = 'URL Setup'
        verbose_name_plural = ' WBGAPI URL'
        
    def __str__(self):
        return "%s" %(self.wbapi_url)



class WorldBankIndicators(models.Model):
    id = models.AutoField(primary_key=True,)  
    code = models.CharField(max_length=45,verbose_name ='Indicator Code',
        blank=False, null=False,default=None)
    name = models.CharField(max_length=255,verbose_name ='Indicator Name',
        default=None)
    reference = models.CharField(max_length=100,blank=True, null=True, 
        verbose_name ='Indicator Reference',default ='World Bank Development Indicators',)

    class Meta:
        managed = True
        db_table = 'worldbank_indicators'
        unique_together = ('code','name',) #enforces concatenated unique constraint
        verbose_name = 'Indicator'
        verbose_name_plural = 'Indicators'
        ordering = ('name',)
    
    def __str__(self):
        return self.name



class WorldBankCountries(models.Model):
    latitude_regex = RegexValidator(
        regex=r'^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)$', message="Enter valid Latitude")
    longitude_regex = RegexValidator(
        regex=r'^[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$',
        message="Enter valid Longitude")
    id = models.AutoField(primary_key=True,)     
    code = models.CharField(max_length=45,verbose_name ='Country Code',
         blank=False, null=False,default=None)
    name = models.CharField(max_length=255,verbose_name ='Country Name',
        default=None)
    latitude = models.DecimalField(_('Latitude'),blank=True, null=True,
        max_digits=15,decimal_places=12,validators=[latitude_regex])
    longitude = models.DecimalField(_('Longitude'),blank=True, null=True,
        max_digits=15,decimal_places=12,validators=[longitude_regex])    
    region = models.CharField(max_length=45,blank=True,null=True,
         verbose_name ='Region')
    incomelevel = models.CharField(max_length=45,blank=True,null=True,
         verbose_name ='Income Level')
    capital = models.CharField(max_length=45,blank=True,null=True,
         verbose_name ='Capital City')

    class Meta:
        managed = True
        db_table = 'worldbank_countries'
        unique_together = ('code','name',) #enforces concatenated unique constraint
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        ordering = ('name',)

    def __str__(self):
        return self.name



# class WorldBank_URLEndpointPath(models.Model):
#     CHOICES=((1,"Active"),(0,"Innactive"))
#     id = models.AutoField(primary_key=True)   
#     url = models.ForeignKey(WBGAPIConfigs, models.CASCADE,
#         verbose_name = 'World Bank URL')
#     api_endpoint = models.CharField(verbose_name='Indicator API Endpoint',
#         max_length=250,blank=True,null=False)
#     status = models.BooleanField(choices=CHOICES,blank=False,
#         verbose_name='Status',)
#     date_created = models.DateTimeField(blank=True, null=True, 
#         auto_now_add=True,verbose_name = 'Date Created')
#     date_lastupdated = models.DateTimeField(blank=True, 
#         null=True,auto_now=True,
#         verbose_name = 'Date Modified')

#     class Meta:
#         managed = True
#         db_table = 'ghoapi_path_endpoint'
#         verbose_name = ' Endpoint'
#         verbose_name_plural = 'Map Endpoints'
#         ordering = ('url',)

#     def __str__(self):
#          return str(self.url)


#     def clean(self):
#         if self.status:
#             active = WorldBank_URLEndpointPath.objects.filter(status=1)
#             if self.pk:
#                 active = active.exclude(pk=self.pk)
#             if active.exists():
#                 raise ValidationError("Only one record can be active at a time")
