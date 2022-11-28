from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

from dhis2metadata.views import (DHIS2APIPathManagementView as dhisapi,
    DHIS2MetadataManagementView as dhismeta,)
from dctmetadata.views import (DCTAPIPathManagementView as dctpv,
    DCTMetadataManagementView as dctmeta)

from ghometadata.views import (GHOMetadataManagementView as ghometa)

from schema_mappings.views import (FactDataIndicatorViewSet as dataview,)
from gho_mappings.views import (FactGHODataIndicatorViewSet as ghoview)
from home import views as login_view


urlpatterns = [
    path('', login_view.index,name='index'),  
    path('accounts/login/', login_view.login_view, name='login'),
    path('admin/', admin.site.urls),
    path('datawizard/', include('data_wizard.urls')), #for data import wizard
    path('api/dhis/path/',dhisapi.as_view({'get':'list'})), 
    path('api/dhis/meta/',dhismeta.as_view()),  
    path('api/dct/path/',dctpv.as_view({'get':'list'})),
    path('api/dct/meta/',dctmeta.as_view()),  
    path('api/gho/meta/',ghometa.as_view()),  
    path('api/data/facts-indicators/',dataview.as_view({'get': 'list'})), 
    path('api/data/gho-facts/',ghoview.as_view({'get': 'list'})), 
    path('api/wb/indicators', include('worldbank_metadata.urls')),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

