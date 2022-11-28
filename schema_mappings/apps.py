from django.apps import AppConfig
from django.conf import settings

class SchemaMappingsConfig(AppConfig):
    name = 'schema_mappings'
    verbose_name = ' DHIS2 Mappings'  

    def ready(self):
        from . jobs import jobscheduler
        if settings.SCHEDULER_AUTOSTART:
            jobscheduler.start()