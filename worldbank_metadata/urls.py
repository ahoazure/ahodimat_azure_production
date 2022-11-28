from django.urls import path
from .views import load_wordbank_indicators

app_name = 'worldbank_metadata'

urlpatterns = [
    path('', load_wordbank_indicators, name='wb_indicators'),
]