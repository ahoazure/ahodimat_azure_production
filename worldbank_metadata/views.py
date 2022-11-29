from django.shortcuts import render
from .models import WorldBankCountries,WorldBankIndicators
import MySQLdb # drivers for accessing MySQL database
import pandas as pd
import wbgapi as wb


def load_wordbank_indicators(request):
    # indicators_df=pd.DataFrame(wb.series.list()) # this works miracles need to add index

    indicators_df=pd.DataFrame(wb.series.list(topic=8)) # this works miracles need to add index
    indicators_df.sort_values(by=['value'],inplace=True,ascending=False)
    indicator_records = indicators_df.to_records(index=True)
    try:    
        indicators = [
            WorldBankIndicators(
                code=record['id'],
                name=record['value'],
            )
            for record in indicator_records
        ]
        records = WorldBankIndicators.objects.bulk_create(
            indicators,ignore_conflicts=True,) 
    except(MySQLdb.IntegrityError, MySQLdb.OperationalError,) as e:
        pass 
    except: # ignore othe database related errors
        print('Unknown Error has occured') 
   


    countries_df=wb.economy.DataFrame(wb.region.members('AFR')) # this works miracles
    countries_df.sort_values(by=['name'],inplace=True,ascending=False)   
    countries_records = countries_df.to_records(index=True)
    try:    
        economies = [
            WorldBankCountries(
                code=record['id'],
                name=record['name'],
                latitude=record['latitude'],
                longitude=record['longitude'],
                region=record['region'],
                incomelevel=record['incomeLevel'],
                capital=record['capitalCity'],
            )
            for record in countries_records
        ]
        records = WorldBankCountries.objects.bulk_create(
            economies,ignore_conflicts=True,) 
        import pdb; pdb.set_trace()	

    except(MySQLdb.IntegrityError, MySQLdb.OperationalError) as e:
        pass 
    except: # ignore othe database related errors
        print('Unknown Error has occured') 
       # import pdb; pdb.set_trace()	

    indicators_list=wb.series.list(topic=8)





