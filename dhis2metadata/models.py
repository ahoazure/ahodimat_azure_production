from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
# importing several methods from date and dateutil modules.  
from dateutil.relativedelta import * 
from datetime import timedelta
import datetime
from utilities import security # used to encrypt sensitive passwords

from authentication.models import CustomUser


"""
This model makes it earsier to change the base URls for DHIS2.
openHIM and the mediators.
"""
class DHIS2MainConfigs(models.Model):
    CHOICES=((1,"Active"),(0,"Innactive"))

    url_regex = RegexValidator(
        regex=r'https?:\/\/(?:w{1,3}\.)?[^\s.]+(?:\.[a-z]+)*(?::\d+)?(?![^<]*(?:<\/\w+>|\/?>))',
        message="Valid URL:'https://abc.com; or http://abc.com:8000'")

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, models.PROTECT, blank=True,
        verbose_name='Username/Email') 
    dhis2_url = models.CharField(max_length=200,validators=[url_regex],
        verbose_name='DHIS2 URL')
    dhis2_user = models.CharField(max_length=200,blank=True,null=True,
        verbose_name='Username') #auth user
    dhis2_passkey = models.CharField(max_length=300,verbose_name='Password') #auth pass
    status = models.BooleanField(choices=CHOICES,verbose_name='Status',
        default=CHOICES[0][0])
    
    class Meta:
        managed = True
        db_table = 'dhis2_main_configs'
        verbose_name = 'DHIS2 Setup'
        verbose_name_plural = 'DHIS2 Settings'
        
    def __str__(self):
        return "%s" %(self.dhis2_url)


    def encrypt_password(self):
        password = security.encrypt(self.dhis2_passkey)
        return password


    def clean(self):
        if (self.dhis2_url.endswith('/')):
            raise ValidationError({'dhis2_url':_(
                'Invalid Base URL. A valid DHIS2 Base URL should NOT have a \
                    forward slash (/) at the end!')}) 
        

    def save(self, *args, **kwargs):
        self.dhis2_passkey = self.encrypt_password()
        super(DHIS2MainConfigs, self).save(*args, **kwargs)



class DHIS2Indicators(models.Model):
    id = models.AutoField(primary_key=True)  # Field name made lowercase
    uid = models.CharField(unique=True,max_length=15,
         verbose_name ='Indicator UID')
    code = models.CharField(max_length=45,blank=True, null=True,)
    name = models.CharField(max_length=255)
    description = models.TextField(verbose_name ='Indicator Description',
        default ='DHIS2',blank=True, null=True,)
    reference = models.CharField(max_length=255, 
        verbose_name ='Indicator Reference',default ='DHIS2',
        blank=True, null=True,)
        
    def __str__(self):
        return self.name # to confirm later  

    class Meta:
        managed = True
        db_table = 'dhis2_indicators'
        verbose_name = 'Indicator'
        verbose_name_plural = 'Indicators'
        ordering = ('name',)
    

class OrganizationUnits(models.Model):
    id = models.AutoField(primary_key=True,verbose_name ='Fact ID')    
    uid = models.CharField(unique=True,max_length=45,
         verbose_name ='OrgUnit UID')
    code = models.CharField(max_length=45,blank=True,null=True,
        verbose_name ='Orgunit Code',default=None)
    name = models.CharField(max_length=255,blank=True,
        null=True,verbose_name ='Country Name')

    class Meta:
        managed = True
        db_table = 'dhs2_orgunits'
        verbose_name = 'Organization Unit'
        verbose_name_plural = ' Organization Units'
        ordering = ('id','name')

    def __str__(self):
        return self.name # to confirm later


class PeriodType(models.Model):
    TYPE = (
        (1,'Fixed'),
        (2,'Relative'),)
    id = models.AutoField(primary_key=True,verbose_name='Period ID')
    name = models.CharField(max_length=50,verbose_name='Period Name')
    shortname = models.CharField(max_length=50, blank=True,
        null=True,verbose_name='Short Name')
    type = models.SmallIntegerField(('Period Type'),choices=TYPE,
        default=TYPE[0][0])
    description = models.TextField(blank=True, null=True,)
    date_created = models.DateTimeField(blank=True, null=True,
        auto_now_add=True,verbose_name = 'Date Created')
    date_lastupdated = models.DateTimeField(blank=True, null=True, 
        auto_now=True,verbose_name = 'Date Modified')

    class Meta:
        managed = True
        db_table = 'dhis2_periods'
        verbose_name = 'Period Type'
        verbose_name_plural = 'Period Types'
        ordering = ('id',)

    def __str__(self):
        return self.name 

    def clean(self):
        if PeriodType.objects.filter(
            name=self.name).count() and not self.id:
            raise ValidationError({'name':'This Period type exists'})

    def save(self, *args, **kwargs):
        super(PeriodType, self).save(*args, **kwargs)


class DHIS2_URLEndpointPath(models.Model):
    CHOICES=((1,"Active"),(0,"Innactive"))
    id = models.AutoField(primary_key=True)   
    url = models.ForeignKey(DHIS2MainConfigs, models.CASCADE,
        verbose_name = 'DHIS2 URL')
    api_endpoint = models.CharField(verbose_name='API Endpoint',
        max_length=250,blank=True,null=False)
    status = models.BooleanField(choices=CHOICES,verbose_name='Status',
        blank=False,)
    date_created = models.DateTimeField(blank=True, null=True, auto_now_add=True,
        verbose_name = 'Date Created')
    date_lastupdated = models.DateTimeField(blank=True, null=True,auto_now=True,
        verbose_name = 'Date Modified')

    class Meta:
        managed = True
        db_table = 'dhis2_api_endpoints'
        verbose_name = 'API Endpoint:'
        verbose_name_plural = 'Map API Endpoints'
        ordering = ('url',)

    def __str__(self):
         return str(self.url)


    def clean(self):
        if not (self.api_endpoint.startswith('/')):
            raise ValidationError({'api_endpoint':_(
                'Invalid API Endpoint! A valid endpoint must start with a forward slash (/)')})    
        
        if self.status:
            active = DHIS2_URLEndpointPath.objects.filter(status=1)
            if self.pk:
                active = active.exclude(pk=self.pk)
            if active.exists():
                raise ValidationError("Only one record can be active at a time")



class DHIS2_URLEndpointPathMapped(models.Model):
    id = models.AutoField(primary_key=True,verbose_name ='Path ID')
    url = models.CharField(max_length=45,verbose_name ='DHIS2 URL',)
    username = models.CharField(max_length=45,)
    password = models.CharField(max_length=300,) 
    endpoint = models.CharField(max_length=100,verbose_name ='Resource Path')  
    api_endpoint = models.CharField(max_length=2083,verbose_name ='Resource URL Endpoint')      
    status = models.PositiveSmallIntegerField(blank=True,null=False,
        verbose_name ='Status',default=0)     

    class Meta:
        managed = False
        db_table = 'vw_dhis2_mapped_api_endpoint'
        verbose_name = 'Mapped API'
        verbose_name_plural = 'Mapped API'
        ordering = ('endpoint',)
        