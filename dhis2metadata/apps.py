from django.apps import AppConfig
from django.conf import settings


class Dhis2MetadataConfig(AppConfig):
    name = 'dhis2metadata'
    verbose_name = '  DHIS2 Metadata'

    # def ready(self):
    #     from . jobs import dhis2scheduler
    #     if settings.SCHEDULER_AUTOSTART:
    #         dhis2scheduler.start()