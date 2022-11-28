from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
from dateutil.relativedelta import * 
import datetime

from dctmetadata.models import (DCTIndicators,DCTLocations,
   DCT_Categoryoptions,DCT_Datasource,DCT_Measuretype)
from dhis2metadata.models import (DHIS2Indicators,OrganizationUnits,
    PeriodType)



STATUS_CHOICES = ( # choices for data approval by authorized users
    ('pending', _('Pending')),
    ('approved',_('Approved')),
    ('rejected',_('Rejected')),
)

class FactsDHIS2_Indicators(models.Model):
    id = models.AutoField(primary_key=True,verbose_name ='Fact ID')
    indicator = models.ForeignKey(DCTIndicators,models.PROTECT,
        verbose_name ='Indicator ID',default=None)
    location = models.ForeignKey(DCTLocations,models.PROTECT,
        verbose_name ='Country ID',default=None)
    categoryoption = models.ForeignKey(DCT_Categoryoptions,on_delete=models.PROTECT,
        verbose_name ='Disaggregation Option',default=None)   
    datasource = models.ForeignKey(DCT_Datasource,on_delete=models.PROTECT,
        verbose_name ='Datasource ID',default=None)   
    measuremethod = models.ForeignKey(DCT_Measuretype,on_delete=models.PROTECT,
        verbose_name ='Measure Type',default=None)          
    numerator_value = models.DecimalField(max_digits=20, decimal_places=3,
        blank=True, null=True)
    denominator_value = models.DecimalField(max_digits=20,decimal_places=3,
        blank=True, null=True)
    value_received= models.DecimalField(max_digits=20,decimal_places=2,
        blank=False,null=False,default=0.00,verbose_name ='Value Received')
    min_value = models.DecimalField(max_digits=20,decimal_places=3,blank=True,
        null=True)
    max_value = models.DecimalField(max_digits=20,decimal_places=3,blank=True,
        null=True)
    target_value = models.DecimalField(max_digits=20,decimal_places=3,blank=True, 
        null=True)  
    string_value = models.CharField(max_length=200,verbose_name ='String Value',
        blank=True, null=True)    
    start_period = models.DateField(verbose_name ='Start Period',
        blank=True, null=True) 
    end_period = models.DateField(verbose_name ='End Period',
        blank=True, null=True)
    period = models.CharField(max_length=45,verbose_name ='Period',
        blank=True, null=True)
    status = models.CharField(_('Status'),max_length=10, choices= STATUS_CHOICES,
        default=STATUS_CHOICES[0][0])  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'fact_indicator_analytics'
        unique_together = ('indicator','location','period') #enforces concatenated unique constraint
        verbose_name = 'Fact'
        verbose_name_plural = '  Fetched Facts'
        
    def __str__(self):
        return str(self.indicator) # to confirm later


    def get_id(self):
        if self.location is not None or self.location!='':
            id = self.location
        return self.id

    def save(self, *args, **kwargs):
        self.id = self.get_id()
        super(FactsDHIS2_Indicators, self).save(*args, **kwargs)



class FactsDHIS2_IndicatorsMapped(models.Model):
    id = models.AutoField(primary_key=True,verbose_name ='Fact ID')
    indicator = models.PositiveSmallIntegerField(blank=True,null=True,
        verbose_name ='Indicator ID')
    location = models.PositiveSmallIntegerField(blank=True,null=True,
        verbose_name ='Country ID')
    datasource = models.PositiveSmallIntegerField(blank=True,null=True,
        verbose_name ='Datasource ID',default=2)   
    categoryoption = models.PositiveSmallIntegerField(blank=True,null=True,
        verbose_name ='Disaggregation Option',default=29)  
    measuremethod = models.PositiveSmallIntegerField(blank=True,null=True,
        verbose_name ='Measure Type',default=1)             
    numerator_value = models.DecimalField(max_digits=20, decimal_places=3,
        blank=True, null=True)
    denominator_value = models.DecimalField(max_digits=20,decimal_places=3,
        blank=True, null=True)
    value_received= models.DecimalField(max_digits=20,decimal_places=2,
        blank=False,null=False,default=0.00,verbose_name ='Value Received')
    min_value = models.DecimalField(max_digits=20,decimal_places=3,blank=True,
        null=True)
    max_value = models.DecimalField(max_digits=20,decimal_places=3,blank=True,
        null=True)
    target_value = models.DecimalField(max_digits=20,decimal_places=3,blank=True, 
        null=True) 
    string_value = models.CharField(max_length=200,verbose_name ='String Value',
        blank=True, null=True)          
    start_period = models.CharField(max_length=45,verbose_name ='Start Period',
        blank=True, null=True) 
    end_period = models.CharField(max_length=45,verbose_name ='End Period',
        blank=True, null=True)
    period = models.CharField(max_length=45,verbose_name ='Period',
        blank=True, null=True)        
    status = models.CharField(max_length=45,verbose_name ='Status',
        blank=True, null=True)    

    class Meta:
        managed = False
        db_table = 'vw_fact_indicator_analytics'
        verbose_name = 'Mapped Fact'
        verbose_name_plural = ' Mapped Facts'
        

class DHIS2_QueryParameters(models.Model):
    CHOICES=((1,"Active"),(0,"Innactive"))
    id = models.AutoField(primary_key=True)   
    indicator = models.ForeignKey(DHIS2Indicators, models.CASCADE,
        verbose_name = 'DHI2 Indicator')
    dctindicator = models.ForeignKey(DCTIndicators, models.CASCADE,
        verbose_name = 'DCT Indicator')
    location = models.ForeignKey(OrganizationUnits, models.DO_NOTHING,
        verbose_name = 'Organisation')
    periodicity = models.ForeignKey(PeriodType, models.PROTECT,
        verbose_name ='Period Type',default=None,)  
    start_period = models.DateField(verbose_name='Start Date',null=False,
        blank=False, default=None,)
    end_period=models.DateField(verbose_name='End Date',null=True,blank=True,
        default=None,)
    # period = models.CharField(verbose_name='Period',max_length=25,blank=True,
    #     null=False)
    status = models.BooleanField(choices=CHOICES,verbose_name='Status',
        blank=False,)
    date_created = models.DateTimeField(blank=True, null=True, auto_now_add=True,
        verbose_name = 'Date Created')
    date_lastupdated = models.DateTimeField(blank=True, null=True, auto_now=True,
        verbose_name = 'Date Modified')

    class Meta:
        managed = True
        unique_together = ('dctindicator','indicator','location','periodicity') #enforces concatenated unique constraint
        db_table = 'dhis2_query_parameters'
        verbose_name = 'Parameter'
        verbose_name_plural = '  Map Parameters'
        ordering = ('location',)

    def __str__(self):
         return str(self.location)

    def clean(self):
        if self.status:
            active = DHIS2_QueryParameters.objects.filter(status=1)
            if self.pk:
                active = active.exclude(pk=self.pk)
            if active.exists():
                raise ValidationError("Only one record can be active at a time")


class FactsDHIS2_QueryParametersMapped(models.Model):
    id = models.AutoField(primary_key=True,verbose_name ='Parameter ID')
    pt = models.CharField(max_length=45,verbose_name ='Period Type',)
    dx = models.CharField(max_length=45,verbose_name ='Data Dimension',)
    ou = models.CharField(max_length=45,verbose_name ='Organisation Unit') 
    status = models.PositiveSmallIntegerField(blank=True,null=True,
        verbose_name ='Status',default=0)     
    startDate = models.DateField(verbose_name ='Start Date',
        blank=True, null=True) 
    endDate = models.DateField(max_length=45,verbose_name ='End Date',
        blank=True, null=True)
    periodname = models.CharField(max_length=100,verbose_name ='Period Type')     
    dct_indicator = models.PositiveSmallIntegerField(blank=True,null=True,
        verbose_name ='Mapped Indicator') 
    period = models.CharField(max_length=45,verbose_name ='Period',
        blank=True, null=True)        

    class Meta:
        managed = False
        db_table = 'vw_dhis2_query_parameters'
        unique_together = ('id','pt',) 
        verbose_name = 'Parameter'
        verbose_name_plural = ' Mapped Parameters'
        ordering = ('id',)
        



class DHIS2DCT_MapOrgunitLocations(models.Model):
    id = models.AutoField(primary_key=True,verbose_name ='Location ID')
    orgunit = models.OneToOneField(OrganizationUnits, models.DO_NOTHING,
        verbose_name = 'DHIS2 Organisation Unit')    
    location = models.OneToOneField(DCTLocations,models.PROTECT,
        verbose_name ='DCT Related Location',default=None)           

    class Meta:
        managed = True
        db_table = 'dhis2_ahodimat_map_orunitlocations'
        unique_together = ('orgunit','location',) #enforces unique constraint
        verbose_name = 'Country'
        verbose_name_plural = 'Map Countries'
        ordering = ('location',)


    def __str__(self):
         return str(self.location)    


class DHIS2DCT_LocationsMapped(models.Model):
    id = models.AutoField(primary_key=True,verbose_name ='Location ID')
    location_name = models.CharField(max_length=45,verbose_name ='Location Name',)
    country_code = models.CharField(max_length=45,verbose_name ='Location Code') 
    locationlevel = models.PositiveSmallIntegerField(blank=True,null=True,
        verbose_name ='Location Level',default=0)     
    dhis_uid = models.CharField(max_length=100,verbose_name ='DHIS2 UID')     
    dhis_code = models.CharField(max_length=45,verbose_name ='DHIS2 CODE',
        blank=True, null=True)        

    class Meta:
        managed = False
        db_table = 'vw_ahodimat_locations_mapped'
        verbose_name = 'Country'
        verbose_name_plural = 'Mapped Countries'
        ordering = ('location_name',)



class DHIS2DCT_IndicatorsMapped(models.Model):
    id = models.AutoField(primary_key=True,verbose_name ='Indicator ID')
    dct_indicator_name = models.CharField(max_length=45,verbose_name ='DCT Indicator Name',)
    afrocode = models.CharField(max_length=45,verbose_name ='DCT Indicator Code')    
    dhis2_indicator = models.CharField(max_length=100,verbose_name ='DHIS2 Indicator Name')     
    dhis_indicator_uid = models.CharField(max_length=45,verbose_name ='DHIS2 Indicator ID',
        blank=True, null=True)
    dct_indicator_id = models.PositiveIntegerField(verbose_name ='DCT Indicator ID')          

    class Meta:
        managed = False
        db_table = 'vw_dhis2dct_indicators_mapped'
        verbose_name = 'Country'
        verbose_name_plural = 'Mapped Indicators'
        ordering = ('dct_indicator_name',)
