from django.db import models

from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
from dateutil.relativedelta import * 
import datetime

from ghometadata.models import (GHOIndicators,GHOSpatialDimensionCountries,
    GHOAPIConfigs,GHO_URLEndpointPath,GHO_URLEndpointPathMapped)
    
from dhis2metadata.models import (PeriodType)
from dctmetadata.models import (DCTIndicators,DCTLocations,
   DCT_Categoryoptions,DCT_Datasource,DCT_Measuretype)

STATUS_CHOICES = ( # choices for data approval by authorized users
    ('pending', _('Pending')),
    ('approved',_('Approved')),
    ('rejected',_('Rejected')),
)


class GHO_IndicatorFacts(models.Model):
    id = models.AutoField(primary_key=True)
    indicator = models.CharField(max_length=100,blank=True,null=True,
        verbose_name ='Indicator Code')
    location = models.CharField(max_length=100,blank=True,null=True,
        verbose_name ='Country')
    category = models.CharField(max_length=45,blank=True,null=True,
        verbose_name ='Disaggregation Type',default=29)       
    categoryoption = models.CharField(max_length=45,blank=True,null=True,
        verbose_name ='Disaggregation Option',default=29)  
    numeric_value= models.CharField(max_length=45,
        blank=True,null=True,verbose_name ='Numeric Value')
    adjusted_value = models.CharField(max_length=45,
        blank=True, null=True)
    min_value = models.CharField(max_length=45,blank=True,
        null=True)
    max_value = models.CharField(max_length=45,blank=True,
        null=True)
    period_type = models.CharField(max_length=45,verbose_name ='Year',
        blank=True, null=True) 
    start_period = models.DateField(verbose_name ='Start Period',
        blank=True, null=True) 
    end_period = models.DateField(verbose_name ='End Period',
        blank=True, null=True)
    period = models.CharField(max_length=45,verbose_name ='Period',
        blank=True, null=True) 
    class Meta:
        managed = True
        db_table = 'gho_indicator_facts_extracted'
        verbose_name = 'GHO Facts'
        verbose_name_plural = '  Fetched Facts'
        
    def __str__(self):
        return str(self.indicator) # to confirm later


    def get_id(self):
        if self.location is not None or self.location!='':
            id = self.location
        return self.id

    def save(self, *args, **kwargs):
        self.id = self.get_id()
        super(GHO_IndicatorFacts, self).save(*args, **kwargs)


class FactsGHO_IndicatorsMapped(models.Model):
    id = models.AutoField(primary_key=True,verbose_name ='Fact ID')
    indicator_code = models.CharField(max_length=200,blank=True,null=True,
        verbose_name ='Indicator Code')
    indicator_name = models.CharField(max_length=200,blank=True,null=True,
        verbose_name ='Indicator Name')
    country = models.CharField(max_length=200,blank=True,null=True,
        verbose_name ='Country Name')  
    category = models.CharField(max_length=200,blank=True,null=True,
        verbose_name ='Disaggrergation category',default=1)   
    categoryoption = models.PositiveSmallIntegerField(blank=True,null=True,
        verbose_name ='Disaggregation Option',default=29)          
    value_received = models.DecimalField(max_digits=20, decimal_places=3,
        blank=True, null=True)
    min_value = models.DecimalField(max_digits=20,decimal_places=3,blank=True,
        null=True)
    max_value = models.DecimalField(max_digits=20,decimal_places=3,blank=True,
        null=True)   
    start_period = models.CharField(max_length=45,verbose_name ='Start Period',
        blank=True, null=True) 
    end_period = models.CharField(max_length=45,verbose_name ='End Period',
        blank=True, null=True)
    period = models.CharField(max_length=45,verbose_name ='Period',
        blank=True, null=True)          

    class Meta:
        managed = False
        db_table = 'vw_gho_fact_indicators'
        verbose_name = 'Stage Fact'
        verbose_name_plural = ' Staged Facts'


class FactsGHODCT_Indicators(models.Model):
    id = models.AutoField(primary_key=True,verbose_name ='Fact ID')
    indicator = models.ForeignKey(DCTIndicators,models.PROTECT,
        verbose_name ='Indicator ID')
    location = models.ForeignKey(DCTLocations,models.PROTECT,
        verbose_name ='Country ID')
    categoryoption = models.ForeignKey(DCT_Categoryoptions,on_delete=models.PROTECT,
        verbose_name ='Disaggregation Option',default=29)   
    datasource = models.ForeignKey(DCT_Datasource,on_delete=models.PROTECT,
        verbose_name ='Datasource ID',default=3)   
    measuremethod = models.ForeignKey(DCT_Measuretype,on_delete=models.PROTECT,
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
        db_table = 'fact_ghodct_indicator_dataset'
        unique_together = ('indicator','location','categoryoption','period',) #enforces concatenated unique constraint
        verbose_name = 'GHO-DCT fact'
        verbose_name_plural = ' Map Facts'
        
    def __str__(self):
        return str(self.indicator) # to confirm later


    def get_id(self):
        if self.location is not None or self.location!='':
            id = self.location
        return self.id

    def save(self, *args, **kwargs):
        self.id = self.get_id()
        super(FactsGHODCT_Indicators, self).save(*args, **kwargs)



class FactsGHO_IndicatorsViewMapped(models.Model):
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
    start_period = models.PositiveSmallIntegerField(verbose_name ='Start Period',
        blank=True, null=True) 
    end_period = models.PositiveSmallIntegerField(verbose_name ='End Period',
        blank=True, null=True)
    period = models.CharField(max_length=45,verbose_name ='Period',
        blank=True, null=True)        
    status = models.CharField(max_length=45,verbose_name ='Status',
        blank=True, null=True)    

    class Meta:
        managed = False
        db_table = 'vw_postghodct_fact_indicators'
        verbose_name = 'Map Fact'
        verbose_name_plural = 'Mapped Facts'