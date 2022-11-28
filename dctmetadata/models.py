from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from utilities import security # used to encrypt sensitive passwords

# from mainconfigs.models import DHIS2UserLocation 
from authentication.models import CustomUser


class DCTConfigs(models.Model):   
    CHOICES=((1,"Active"),(0,"Innactive"))
    url_regex = RegexValidator(
        regex=r'https?:\/\/(?:w{1,3}\.)?[^\s.]+(?:\.[a-z]+)*(?::\d+)?(?![^<]*(?:<\/\w+>|\/?>))',
        message="Valid URL:'https://abc.com; or http://abc.com:8000'")

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, models.PROTECT, blank=True,
        verbose_name='Username/Email')        
    dct_url = models.CharField(max_length=200,validators=[url_regex],
        verbose_name='DCT URL') #base url
    dct_user = models.CharField(max_length=200, verbose_name='Username') #auth user
    dct_passkey = models.CharField(max_length=300,verbose_name='Password') #auth pass
    status = models.BooleanField(choices=CHOICES,verbose_name='Status',
        default=CHOICES[0][0])
    
    class Meta:
        managed = True
        db_table = 'ahodct_configs'
        verbose_name = 'DCT Setup'
        verbose_name_plural = 'DCT Settings'
        
    def __str__(self):
        return "%s " %(self.dct_url)

    def encrypt_password(self):
        password = security.encrypt(self.dct_passkey)
        return password


    # Override Save method to store only one instance
    def save(self, *args, **kwargs):
        self.dct_passkey = self.encrypt_password()
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super(DCTConfigs, self).save(*args, **kwargs)



class DCTIndicators(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True,
        verbose_name ='Indicator ID')
    # dhis2= models.ManyToManyField(DHIS2Indicators,blank=True,)
    code = models.CharField(max_length=45,blank=True, null=True,)
    name = models.CharField(max_length=255)
    description = models.TextField(verbose_name ='Description',
        default ='DCT indicator',blank=True, null=True,)
    reference = models.CharField(max_length=255, 
        verbose_name ='Indicator Source',default ='DCT',
        blank=True, null=True,)

    class Meta:
        managed = True
        db_table = 'dct_indicators'
        verbose_name = 'Indicator'
        verbose_name_plural = 'Indicators'
        ordering = ('name',)
    
    def __str__(self):
        return self.name


class DCTLocations(models.Model):
    id = models.AutoField(primary_key=True,verbose_name ='LocID')
    location_id = models.PositiveSmallIntegerField(blank=True,null=True,
        verbose_name ='Location ID')        
    code = models.CharField(max_length=45,blank=True,null=True,
        verbose_name ='Location Code')
    name = models.CharField(max_length=255,blank=True,
        null=True,verbose_name ='Country Name')
    locationlevel = models.CharField(max_length=45,blank=True,null=True,
         verbose_name ='Level')
    # dhis2orgunit= models.OneToOneField(OrganizationUnits, models.CASCADE,
    #     verbose_name ='DHIS2 Orgunit',blank=True,null=True) #only one match is required

    class Meta:
        managed = True
        db_table = 'afro_locations'
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
        ordering = ('id',)

    def __str__(self):
        return self.name


class DCT_Categoryoptions(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True,)
    category= models.PositiveIntegerField(blank=True,
        verbose_name ='Category ID',default=29)
    code = models.CharField(max_length=45,blank=True, null=True,)
    name = models.CharField(max_length=255)
    description = models.TextField(verbose_name ='Description',
        default ='DCT Disaggregation',blank=True, null=True,)
    reference = models.CharField(max_length=255, 
        verbose_name ='Disaggregation Options',default ='DCT',
        blank=True, null=True,)

    class Meta:
        managed = True
        db_table = 'dct_categoryoptions'
        verbose_name = 'Category Option'
        verbose_name_plural = 'Category Options'
        ordering = ('name',)
    
    def __str__(self):
        return self.name


class DCT_Datasource(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True,
        verbose_name ='Datasource ID')
    code = models.CharField(max_length=45,blank=True, null=True,)
    name = models.CharField(max_length=255)
    description = models.TextField(verbose_name ='Description',
        default ='DCT Datasource',blank=True, null=True,)
    reference = models.CharField(max_length=255, 
        verbose_name ='Data Source',default ='DCT',
        blank=True, null=True,)

    class Meta:
        managed = True
        db_table = 'dct_datasource'
        verbose_name = 'Data Source'
        verbose_name_plural = 'Data Sources'
        ordering = ('name',)
    
    def __str__(self):
        return self.name


class DCT_Measuretype(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True,
        verbose_name ='Measure ID')
    code = models.CharField(max_length=45,blank=True, null=True,)
    name = models.CharField(max_length=255)
    description = models.TextField(verbose_name ='Description',
        default ='Measure Type',blank=True, null=True,)
    reference = models.CharField(max_length=255, 
        verbose_name ='Measure Reference',default ='DCT',
        blank=True, null=True,)

    class Meta:
        managed = True
        db_table = 'dct_indicator_measuretype'
        verbose_name = 'Measure Type'
        verbose_name_plural = 'Measure Types'
        ordering = ('name',)
    
    def __str__(self):
        return self.name


class DCT_URLEndpointPath(models.Model):
    CHOICES=((1,"Active"),(0,"Innactive"))
    id = models.AutoField(primary_key=True)   
    url = models.ForeignKey(DCTConfigs, models.CASCADE,
        verbose_name = 'DCT URL')
    api_endpoint = models.CharField(verbose_name='API Endpoint',
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
        db_table = 'dct_path_endpoint'
        verbose_name = 'Map Endpoint:'
        verbose_name_plural = 'Map Endpoints'
        ordering = ('url',)

    def __str__(self):
         return str(self.url)


    def clean(self):
        if self.status:
            active = DCT_URLEndpointPath.objects.filter(status=1)
            if self.pk:
                active = active.exclude(pk=self.pk)
            if active.exists():
                raise ValidationError("Only one record can be active at a time")


class DCT_URLEndpointPathMapped(models.Model):
    id = models.AutoField(primary_key=True,verbose_name ='Path ID',)
    url = models.CharField(max_length=45,verbose_name ='DCT URL',)
    username = models.CharField(max_length=45,)
    password = models.CharField(max_length=300,) 
    endpoint = models.CharField(max_length=100,verbose_name ='Resource Path')    
    resource_endpoint = models.CharField(
        max_length=2083,verbose_name ='Resource URL Endpoint')       
    status = models.PositiveSmallIntegerField(blank=True,null=False,
        verbose_name ='Status',default=0)     

    class Meta:
        managed = False
        db_table = 'vw_dct_apipath_endpoint'
        verbose_name = 'Mapped Endpoint'
        verbose_name_plural = 'Mapped Endpoints'
        ordering = ('url',)
        
