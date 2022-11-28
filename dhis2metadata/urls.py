"""
dhis2dct_integration URL Configuration
"""
from django.contrib import admin
from django.urls import path,include
# from rest_framework.urlpatterns import format_suffix_patterns

from dhis2metadata.views import (DHIS2IndictorsManagementView as dhis,)

urlpatterns = [
    path('api/dhis/indicators/',dhis.as_view()), 
    # path('api/dct/locations/',dctlv.as_view()),   
]
