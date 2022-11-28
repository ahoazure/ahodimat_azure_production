from django.contrib import admin
from django.forms import TextInput,Textarea 
from import_export.admin import ImportExportModelAdmin,ExportActionModelAdmin
from .models import (GHO_IndicatorFacts,FactsGHO_IndicatorsMapped,
    FactsGHODCT_Indicators,FactsGHO_IndicatorsViewMapped)

import data_wizard # Solution to data import from GHO API fetch

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


@admin.register(GHO_IndicatorFacts)
class GHOIndicatorFactsAdmin(ImportExportModelAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    fieldsets = (
       ('Indicator Fact Details',{
            'fields': (
                'indicator','location','category','categoryoption',
                'numeric_value','adjusted_value','min_value',
                'max_value','period_type','start_period','end_period',
                'period',)
            }),
        )
    # filter_horizontal = ('dhis2',)
    list_display = ('indicator','location','category','categoryoption',
                    'numeric_value','adjusted_value','start_period',
                    'end_period','period', )
    search_fields = ('indicator','location')
    # readonly_fields=('name','code','language',)


@admin.register(FactsGHO_IndicatorsMapped)
class GHOFactsViewAdmin(ImportExportModelAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }      
    list_display = ('indicator_name','country','category','categoryoption',
                    'value_received','start_period','end_period','period', )


data_wizard.register(FactsGHODCT_Indicators)
@admin.register(FactsGHODCT_Indicators)
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


@admin.register(FactsGHO_IndicatorsViewMapped)
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
        'numerator_value','denominator_value','value_received','start_period',\
        'end_period','period','status')
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
