#========================================
# Jobs Scheduler Logic
#========================================
from datetime import datetime
import traceback
from django.conf import settings
from django.db.utils import OperationalError
import logging

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.executors.pool import ProcessPoolExecutor,ThreadPoolExecutor
from django_apscheduler.jobstores import register_events,register_job

from dctmetadata.views import (DCTMetadataManagementView as dctm,)
from dhis2metadata.views import (DHIS2MetadataManagementView as dhisim,)
from ghometadata.views import (GHOMetadataManagementView as ghomv,)
from dhis2_mappings.views import (FactDataIndicatorViewSet as schema,)

from gho_mappings.views import (GHOIndicatiorFactsManagementView as ghofm,
  FactGHODataIndicatorViewSet as facts)

# Create scheduler to run in a thread inside the application process
scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG,timezone="Africa/Nairobi")

def start(): ## Add  jobs here using cron trigger instead of to interval.
    if settings.DEBUG:
        logging.basicConfig()  # Hook into the apscheduler logger
        logging.getLogger('apscheduler').setLevel(logging.DEBUG)
        
        dct_meta=dctm() # instantiate DCT metadata scheduling instance
        dhis_meta=dhisim() # instantiate DHIS2 metadata scheduling instance
        
        fact_indicators =schema() #instantiate transformed facts view class
        gho_meta = ghomv()
        gho_facts = ghofm()
        
    try: 
        dct_meta=dctm() # instantiate DCT metadata scheduling instance
        dhis_meta=dhisim() # instantiate DHIS2 metadata scheduling instance
        
        fact_indicators =schema() #instantiate transformed facts view class
        gho_meta = ghomv()
        gho_facts = ghofm()
        post_facts = facts()

  
        scheduler.add_job(dct_meta.mediators_dct_metadata,'cron',minute='*/30',
          jitter=30,id='Import DCT Metadata',replace_existing=True) 
        scheduler.add_job(dhis_meta.mediators_dhis_metadata,'cron',minute='*/40',
          jitter=20,id='Import DHIS2 Metadata',replace_existing=True)
        
        scheduler.add_job(gho_meta.mediators_gho_metadata,'cron',minute='*/35',
          jitter=30,id='Import GHO Metadata',replace_existing=True)

        scheduler.add_job(gho_facts.mediators_gho_save_dataset,'cron',minute='*/1',
          jitter=30,id='Import GHO Indicator Facts',replace_existing=True)

        scheduler.add_job(fact_indicators.get_dhis_indicatorfacts,'cron',minute='*/45',
          jitter=60,id='Import DHIS2 Indicator Facts',replace_existing=True)    
        
        scheduler.add_job(fact_indicators.post_dctfact_indicators,'cron',minute='*/55',
          jitter=30,id='Export Mapped DHIS2 Facts to DCT',replace_existing=True)

        scheduler.add_job(post_facts.post_ghofact_indicators,'cron',minute='*/59',
          jitter=60,id='Export GHO Mapped Facts to DCT',replace_existing=True)

        register_events(scheduler) # Add scheduled jobs to the admin interface   
        scheduler.start() # Activate the scheduler
    except:
        pass


