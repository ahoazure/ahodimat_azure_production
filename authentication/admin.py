from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput,Textarea 
from django.contrib.admin.models import LogEntry
from import_export.admin import ImportExportModelAdmin

from .models import CustomUser,CustomGroup,MediatorConfigs
from . import models
# from mainconfigs.models import MediatorUserLocation


@admin.register(models.CustomUser)
class UserAdmin (UserAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }

    """
    We don't need to show list of permissions for non superuser admins. They
    just need to assign the groups which already are linked to the permissions
    """
    def get_fieldsets(self, request, obj=None):
          fieldsets = super(UserAdmin, self).get_fieldsets(request, obj)
         # This method hides permsions and super use attributes on the model form
          remove_fields = ['user_permissions','is_superuser']
          if not request.user.is_superuser:
              if len(fieldsets) > 0:
                  for f in fieldsets:
                      if f[0] == 'Account Permissions':
                          fieldsets[2][1]['fields'] = tuple(
                              x for x in fieldsets[2][1]['fields']
                              if not x in remove_fields)
                          break
          return fieldsets

    """
    For non-superusers, eg. Country admins, if they need to assign groups to
    other users, we only need to show groups in the Country admins location
    """
    def get_form(self, request, obj=None, **kwargs):
          form = super(UserAdmin, self).get_form(request, obj, **kwargs)
          if not request.user.is_superuser:
              filtered_groups = CustomGroup.objects.filter(
                  roles_manager=request.user.id)
              if form.base_fields.get('groups'):
                  form.base_fields['groups'].queryset=CustomGroup.objects.filter(
                      user=request.user.id)
          return form

    """
    The purpose of this method is to delegate limited role of creatting users
    and groups to a non-superuser. This is achieved by assigning logged in user
    location to the user being created.
    """
    def save_model(self, request, obj, form, change):
        req_user = request.user.id
        if not req_user:
            obj.roles_manager = req_user
        super().save_model(request, obj, form, change)

    """
    The purpose of this method is to filter displayed list of users to location
    of logged in user
    """
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Get a query of groups the user belongs and flatten it to list object
        group = list(request.user.groups.values_list('user', flat=True))
        if request.user.is_superuser:
            qs # return all objecis in the request
        else:
            qs=qs.filter(id__in=group)
        return qs

    readonly_fields = ('last_login','date_joined',)
    fieldsets = (
        ('Personal info', {'fields': ('title','first_name', 'last_name',
            'gender',)}),
        ('Login Credentials', {'fields': ('email', 'username',)}),
        ('Account Permissions', {'fields': ('is_active', 'is_staff',
            'is_superuser', 'groups', 'user_permissions')}),
        ('Login Details', {'fields': ('last_login',)}),
    )
    limited_fieldsets = (
        ('Persional Details', {'fields': ('email',)}),
        ('Personal info', {'fields': ('first_name', 'last_name',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        ('Contacts and Password', {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    list_display = ['first_name','last_name','gender','email','username',
        'last_login']
    list_display_links = ['first_name','last_name','username','email']


admin.site.unregister(Group)# Unregister the group in order to use custom group
@admin.register(models.CustomGroup)
class GroupAdmin(BaseGroupAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Get a query of groups the user belongs and flatten it to list object
        groups = list(request.user.groups.values_list('user', flat=True))
        user = request.user.id
        
        if request.user.is_superuser:
            qs # return all instances of the request instances
        elif user in groups:
            qs=qs.filter(user=user)
        return qs

    """
    The purpose of this method is to restrict display of permission selections
    in the listbox. Only permissions asigned to logged in user group are loaded.
    """
    def get_form(self, request, obj=None, **kwargs):
        form = super(GroupAdmin, self).get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            filtered_groups = CustomGroup.objects.filter(
                user=request.user.id)
            user_permissions = [f.permissions.all() for f in filtered_groups][0]
            if form.base_fields.get('permissions'):
                form.base_fields['permissions'].queryset = user_permissions
        return form

    # Override get_changeform_initial_data to autofill user field with logged user
    def get_changeform_initial_data(self, request):
        get_data = super(
        GroupAdmin,self).get_changeform_initial_data(request)
        get_data['roles_manager'] = request.user
        return get_data

    """
    Overrride model_save method to grab id of the logged in user. The save_model
    method is given HttpRequest (request), model instance (obj), ModelForm
    instance (form), and boolean value (change) based on add or changes to object.
    """
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.roles_manager = request.user # set user during the first save.
        super().save_model(request, obj, form, change)

    exclude = ['roles_manager',]
    list_display = ['name','roles_manager']
    list_select_related = ('role',)



@admin.register(MediatorConfigs)
class ConfigAdmin(ImportExportModelAdmin):
    from django.db import models

    # Make the password field read only to avoid any changes after encryption
    def get_readonly_fields(self, request, obj=None):
        if obj: # check if the object is null rhen diable password
            return ['openhim_passkey']
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if obj.pk: # If record exists, ingore saving encrypted password
            obj.openhim_passkey = None 
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
       ('Mediator Connection Details', {
            'fields': ('mediator_url','mediator_port', 
            'openhim_url','openhim_port','openhim_user',
            'openhim_passkey','status',),
        }),      
    )

    list_display=['mediator_url','mediator_port','openhim_url','status']
    list_select_related = ('user',)
    list_display_links = ('mediator_url',) 
    search_fields = ('mediator_url',) 
    exclude = ('date_created','date_lastupdated',)