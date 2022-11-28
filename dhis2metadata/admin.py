from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.forms import TextInput,Textarea

from .models import (DHIS2Indicators,OrganizationUnits,
        PeriodType,DHIS2_URLEndpointPath,DHIS2Configs,
        DHIS2_URLEndpointPathMapped)


@admin.register(DHIS2Configs)
class ConfigAdmin(ImportExportModelAdmin):
    from django.db import models

    # Make the password field read only to avoid any changes after encryption
    def get_readonly_fields(self, request, obj=None):
        if obj: # check if the object is null rhen diable password
            return ['dhis2_passkey']
        return self.readonly_fields
        
    def save_model(self, request, obj, form, change):
        if obj.pk: # If record exists, ingore saving encrypted password
            obj.dhis2_passkey = None         
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
       ('DHIS2 Connection Details',{
           'fields': (
               'dhis2_url','dhis2_user',
               'dhis2_passkey','status',)
        }),       
    )

    list_display=['dhis2_url','status',]
    list_select_related = ('user',)
    list_display_links = ('dhis2_url',) 
    search_fields = ('dhis2_url',) 
    exclude = ('date_created','date_lastupdated',)



@admin.register(DHIS2Indicators)
class DHIS2IndicatorsAdmin(ImportExportModelAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    fieldsets = (
       ('Indicator Details',{
           'fields': (
                'name','uid','code','description',
                'reference',)
         }),)
    list_display = ('name','uid','reference',)
    search_fields = ('uid','name',)
    list_display_links=('uid','name')


@admin.register(OrganizationUnits)
class OrganizationAdmin(ImportExportModelAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    fieldsets = (
       ('Organization Unit Details',{
           'fields': (
                'name','uid','code',)
         }),)

    list_display = ('name','uid','code',)
    list_display_links=('uid','name')


@admin.register(PeriodType)
class PeriodtypeAdmin(ImportExportModelAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }

    fieldsets = (
       ('Organixation Unit Details',{
           'fields': (
                'name','type','description',)
         }),)

    list_display=['name','type','description',]
    search_fields = ('name','type',)
    exclude = ('date_created','date_lastupdated',)
    list_display_links=('name','type')


@admin.register(DHIS2_URLEndpointPath)
class DHIS2URLPathAdmin(ImportExportModelAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }

    list_display = ('url','api_endpoint','status',)
    list_display_links=('url','api_endpoint')



@admin.register(DHIS2_URLEndpointPathMapped)
class DHIS2APIPathAdmin(ImportExportModelAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }

    list_display = ('url','endpoint','api_endpoint','is_status')
    list_display_links=('url','endpoint')

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