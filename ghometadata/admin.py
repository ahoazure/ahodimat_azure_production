from django.contrib import admin

from django.forms import TextInput,Textarea 
from import_export.admin import ImportExportModelAdmin
from .models import (GHOIndicators,GHOSpatialDimensionCountries,
    GHOMainConfigs,GHO_URLEndpointPath,GHO_URLEndpointPathMapped)


@admin.register(GHOMainConfigs)
class ConfigAdmin(ImportExportModelAdmin):
    from django.db import models
   
    # Make the password field read only to avoid any changes after encryption
    def get_readonly_fields(self, request, obj=None):
        if obj: # check if the object is null rhen diable password
            return ['dct_passkey']
        return self.readonly_fields
        
    def save_model(self, request, obj, form, change):
        if obj.pk: # If record exists, ingore saving encrypted password
            obj.dct_passkey = None 
        if not obj.pk:
            obj.user = request.user # only set user during the first save.
        super().save_model(request, obj,form, change)

    formfield_overrides = {
        models.CharField: {'widget': TextInput(
            attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(
            attrs={'rows':3, 'cols':100})},
    }

    fieldsets = (
       ('DCT Connection Details', {
            'fields':('gho_url','gho_user','gho_passkey','status',),
        }),
    )


    list_display=['gho_url','status']
    list_select_related = ('user',)
    list_display_links = ('gho_url',) 
    search_fields = ('gho_url',) 
    exclude = ('date_created','date_lastupdated',)



@admin.register(GHOIndicators)
class DCTIndicatorsAdmin(ImportExportModelAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    fieldsets = (
       ('Indicator Details',{
            'fields': (
                'name','code','language','reference',)
            }),
        )
    # filter_horizontal = ('dhis2',)
    list_display = ('name','code','language','reference')
    search_fields = ('code','name',)
    readonly_fields=('name','code','language',)


@admin.register(GHOSpatialDimensionCountries)
class OrgDCTLocationsAdmin(ImportExportModelAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    fieldsets = (
       ('Country Details',{
            'fields': (
                'name','code','dimension','parent',)
            }),
        )              
    list_display = ('name','code','dimension','parent',)
    list_display_links =('name','code',)
    readonly_fields=('name','code','dimension',)



@admin.register(GHO_URLEndpointPath)
class DCTURLPathAdmin(ImportExportModelAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    list_display = ('url','api_endpoint','status',)



@admin.register(GHO_URLEndpointPathMapped)
class DHIS2APIPathAdmin(ImportExportModelAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    list_display = ('url','resource_endpoint','is_status')
    list_display_links=('url','resource_endpoint')

    def is_status(self, obj): # Replace boolean values with meaningful text
        yes_flag = "Active"
        no_flag = "Inactive"
        if obj.status:
            return yes_flag
        else:
            return no_flag
    is_status.allow_tags = True
    is_status.short_description = 'Status'

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
        return super(DHIS2APIPathAdmin, self).change_view(
            request,object_id,extra_context=extra_context)  