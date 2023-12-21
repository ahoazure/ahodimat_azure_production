from django.contrib import admin
from django.forms import TextInput,Textarea
from import_export.admin import ImportExportModelAdmin,ExportActionModelAdmin
from .models import (FactsDHIS2_Indicators,FactsDHIS2_IndicatorsMapped,
        FactsDHIS2_QueryParametersMapped,DHIS2DCT_LocationsMapped,
        DHIS2_QueryParameters,DHIS2DCT_IndicatorsMapped,
        DHIS2DCT_MapOrgunitLocations)


#These functions are used to register actions performed on data approval.
def transition_to_pending (modeladmin, request, queryset):
    queryset.update(status = 'pending')
transition_to_pending.short_description = "Mark selected as Pending"

def transition_to_approved (modeladmin, request, queryset):
    queryset.update (status = 'approved')
transition_to_approved.short_description = "Mark selected as Approved"

def transition_to_rejected (modeladmin, request, queryset):
    queryset.update (status = 'rejected')
transition_to_rejected.short_description = "Mark selected as Rejected"


@admin.register(FactsDHIS2_Indicators)
class DHIS2FactsAdmin(ImportExportModelAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }  

    def get_actions(self, request):
        actions = super(DHIS2FactsAdmin, self).get_actions(request)
        if not request.user.has_perm('schema_mappings.approve_factsdhis2_indicators'):
           actions.pop('transition_to_approved', None)
        if not request.user.has_perm('schema_mappings.reject_factsdhis2_indicators'):
            actions.pop('transition_to_rejected', None)
        if not request.user.has_perm('schema_mappings.delete_factsdhis2_indicators'):
            actions.pop('delete_selected', None)
        return actions

    actions = ExportActionModelAdmin.actions + [transition_to_pending,
        transition_to_approved,transition_to_rejected,]

    fieldsets = ( # used to create frameset sections on the data entry form
        ('Indicator Details', {
                'fields': ('indicator','location','categoryoption','datasource',
                'measuremethod',)
            }),
            ('Reporting Period & Data Values', {
                'fields': ('value_received','numerator_value','denominator_value',
                'min_value','max_value','target_value','string_value',
                'start_period','end_period','period','status',),
            }),
        )
    list_display = ('indicator','location','numerator_value',
        'denominator_value','value_received','period','status',)
    

@admin.register(FactsDHIS2_IndicatorsMapped)
class DHIS2FactsViewAdmin(ImportExportModelAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }      
    fieldsets = ( # used to create frameset sections on the data entry form
        ('Indicator Details', {
                'fields': ('indicator','location','categoryoption','datasource',
                'measuremethod',)
            }),
            ('Reporting Period & Data Values', {
                'fields': ('value_received','numerator_value','denominator_value',
                'min_value','max_value','target_value','string_value',
                'start_period','end_period','period',),
            }),
        )

    list_display = ('indicator','location','datasource','categoryoption',
        'numerator_value','denominator_value','value_received','period','status')
    search_fields = ('indicator','location',) #display search field
    #This method removes the add button on the admin interface
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

    def change_view(self, request, object_id, extra_context=None):
        ''' Customize add/edit form '''
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        return super(DHIS2FactsViewAdmin, self).change_view(
            request,object_id,extra_context=extra_context)




@admin.register(DHIS2DCT_MapOrgunitLocations)
class DHIS2DCT_MapOrgunitLocationsAdmin(ImportExportModelAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    } 

    list_display=['orgunit','location',]
    search_fields = ('orgunit','location',) 


@admin.register(DHIS2DCT_LocationsMapped)
class DHIS2DCTLocationsAdmin(ImportExportModelAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }  

    fieldsets = (
       ('Location Details',{
            'fields': (
                'location_name','country_code','locationlevel',
                'dhis_uid',)
            }),
        )  
    list_display = ('location_name','id','country_code','locationlevel',
        'dhis_uid',)
    
    #This method removes the add button on the admin interface
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

    def change_view(self, request, object_id, extra_context=None):
        ''' Customize add/edit form '''
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        return super(DHIS2DCTLocationsAdmin, self).change_view(
            request,object_id,extra_context=extra_context)



@admin.register(DHIS2DCT_IndicatorsMapped)
class DHIS2DCTIndicatorssAdmin(ImportExportModelAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }  

    fieldsets = (
       ('Location Details',{
            'fields': (
                'dct_indicator_name','afrocode','dhis2_indicator',
                'dhis_indicator_uid','dct_indicator_id',)
            }),
        )  
    list_display = ('dct_indicator_name','afrocode','dhis2_indicator',
                    'dhis_indicator_uid','dct_indicator_id',)
    
    #This method removes the add button on the admin interface
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

    def change_view(self, request, object_id, extra_context=None):
        ''' Customize add/edit form '''
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        return super(DHIS2DCTIndicatorssAdmin, self).change_view(
            request,object_id,extra_context=extra_context)




@admin.register(DHIS2_QueryParameters)
class ParameterAdmin(ImportExportModelAdmin):
    pass

    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }

    class Media:
       js = ('https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',
        'js/parameterScript.js',)   
    
    list_display=['dctindicator','indicator','location','periodicity',
        'start_period','end_period','status']
    search_fields = ('indicator','location',) #display search field
    exclude = ('date_created','date_lastupdated',)



@admin.register(FactsDHIS2_QueryParametersMapped)
class DHIS2ParametersAdmin(ImportExportModelAdmin): 
    #This method removes the add button on the admin interface
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

    def change_view(self, request, object_id, extra_context=None):
        ''' Customize add/edit form '''
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        return super(DHIS2ParametersAdmin, self).change_view(
            request,object_id,extra_context=extra_context)   


    def is_status(self, obj): # Replace boolean values with meaningful text
        yes_flag = "Active"
        no_flag = "Inactive"
        if obj.status:
            return yes_flag
        else:
            return no_flag
    is_status.allow_tags = True
    is_status.short_description = 'Status'

    list_display = ('dx','ou','id','pt','dct_indicator','periodname',
    'startDate','endDate','period','is_status')