from django.contrib import admin
from django.forms import TextInput,Textarea 
from import_export.admin import ImportExportModelAdmin
from .models import (DCTIndicators,DCTLocations,
    DCT_URLEndpointPath,DCT_URLEndpointPathMapped,
    DCT_Categoryoptions,DCT_Datasource,
    DCT_Measuretype,DCTConfigs)

@admin.register(DCTConfigs)
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
            'fields':('dct_url','dct_user','dct_passkey',
           'status',),
        }),
    )

    list_display=['dct_url','status']
    list_select_related = ('user',)
    list_display_links = ('dct_url',) 
    search_fields = ('dct_url',) 
    exclude = ('date_created','date_lastupdated',)




@admin.register(DCTIndicators)
class DCTIndicatorsAdmin(ImportExportModelAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    fieldsets = (
       ('Indicator Details',{
            'fields': (
                'name','code','id','reference',)
            }),
        )
    # filter_horizontal = ('dhis2',)
    list_display = ('name','code','id','reference')
    search_fields = ('code','name',)
    readonly_fields=('name','code','id',)


@admin.register(DCTLocations)
class OrgDCTLocationsAdmin(ImportExportModelAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    fieldsets = (
       ('Location Details',{
            'fields': (
                'location_id','code','name','locationlevel',
                )
            }),
        )              
    list_display = ('name','location_id','code','locationlevel',)
    list_display_links =('location_id','name','code',)
    readonly_fields=('name','code','location_id',)


@admin.register(DCT_Categoryoptions)
class DCT_CategoryoptionsAdmin(ImportExportModelAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    fieldsets = (
       ('Location Details',{
            'fields': (
                'name','code','id','category','reference',
                'description',)
            }),
        )              
    list_display = ('name','code','id','category','description',)
    list_display_links =('name','code',)
    readonly_fields=('id','name','code',)


@admin.register(DCT_Datasource)
class DCT_DatasourceAdmin(ImportExportModelAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    fieldsets = (
       ('Location Details',{
            'fields': (
                'name','code','description','reference',
                )
            }),
        )              
    list_display = ('name','code','id','reference','description',)
    list_display_links =('name','code',)
    readonly_fields=('name','code',)



@admin.register(DCT_Measuretype)
class DCT_MeasuretypeAdmin(ImportExportModelAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    fieldsets = (
       ('Location Details',{
            'fields': (
                'name','code','description','reference',
                )
            }),
        )              
    list_display = ('name','code','id','reference','description',)
    list_display_links =('name','code',)
    readonly_fields=('name','code',)



@admin.register(DCT_URLEndpointPath)
class DCTURLPathAdmin(ImportExportModelAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    list_display = ('url','api_endpoint','status',)


@admin.register(DCT_URLEndpointPathMapped)
class DHIS2APIPathAdmin(ImportExportModelAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    list_display = ('url','endpoint','resource_endpoint','is_status')
    list_display_links=('url','resource_endpoint',)

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