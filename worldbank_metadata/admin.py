from django.contrib import admin


from django.forms import TextInput,Textarea 
from import_export.admin import ImportExportModelAdmin
from .models import (WBGAPIConfigs,WorldBankIndicators,WorldBankCountries)


@admin.register(WBGAPIConfigs)
class WorldBankConfigAdmin(ImportExportModelAdmin):
    from django.db import models
    formfield_overrides = {
    models.CharField: {'widget': TextInput(attrs={'size':'100'})},
    models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }

    def get_readonly_fields(self, request, obj=None):
        if obj: # check if the object is null then diable password
            return ['wbapi_passkey']
        return self.readonly_fields
        
    def save_model(self, request, obj, form, change):
        if obj.pk: # If record exists, ingore saving encrypted password
            obj.wbapi_passkey = None 
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
            'fields':('wbapi_url','wbapi_user','wbapi_passkey','status',),
        }),
    )

    list_display=['wbapi_url','status']
    list_select_related = ('user',)
    list_display_links = ('wbapi_url',) 
    search_fields = ('wbapi_url',) 
    exclude = ('date_created','date_lastupdated',)



@admin.register(WorldBankIndicators)
class DCTIndicatorsAdmin(ImportExportModelAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    fieldsets = (
       ('Indicator Details',{
            'fields': (
                'name','code','reference',)
            }),
        )
    # filter_horizontal = ('dhis2',)
    list_display = ('name','code','reference')
    search_fields = ('code','name',)
    readonly_fields=('name','code',)


@admin.register(WorldBankCountries)
class OrgDCTLocationsAdmin(ImportExportModelAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    fieldsets = (
       ('Country Details',{
            'fields': (
                'name','code','region','latitude','longitude',
                'incomelevel','capital',)
            }),
        )              
    list_display = ('name','code','region','latitude','longitude',
        'incomelevel','capital',)
    list_display_links =('name','code',)
    readonly_fields=('name','code','region',)