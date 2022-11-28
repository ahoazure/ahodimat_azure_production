# Generated by Django 3.0.14 on 2022-06-24 09:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dhis2metadata', '0004_auto_20220624_0908'),
    ]

    operations = [
        migrations.CreateModel(
            name='DHIS2DCT_IndicatorsMapped',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='SerialID')),
                ('indicator_id', models.PositiveSmallIntegerField(blank=True, default=0, null=True, verbose_name='Indicator ID')),
                ('indicator_name', models.CharField(max_length=45, verbose_name='Indicator Name')),
                ('afrocode', models.CharField(blank=True, max_length=45, null=True, verbose_name='Indicator Code')),
                ('dhis_uid', models.CharField(max_length=100, verbose_name='DHIS2 UID')),
            ],
            options={
                'verbose_name': 'Indicator',
                'verbose_name_plural': 'Show Indicators',
                'db_table': 'vw_dhis2dct_indicators_mapped',
                'ordering': ('indicator_id',),
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DHIS2DCT_LocationsMapped',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Location ID')),
                ('dct_country', models.CharField(max_length=45, verbose_name='Location Name')),
                ('country_code', models.CharField(max_length=45, verbose_name='Location Code')),
                ('location_level', models.PositiveSmallIntegerField(blank=True, default=0, null=True, verbose_name='Status')),
                ('dhis_uid', models.CharField(max_length=100, verbose_name='DHIS2 UID')),
                ('dhis_code', models.CharField(blank=True, max_length=45, null=True, verbose_name='DHIS2 CODE')),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Show Countries',
                'db_table': 'vw_ahodimat_locations_mapped',
                'ordering': ('id',),
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FactsDHIS2_IndicatorsMapped',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Fact ID')),
                ('indicator', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Indicator ID')),
                ('location', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Country ID')),
                ('datasource', models.PositiveSmallIntegerField(blank=True, default=2, null=True, verbose_name='Datasource ID')),
                ('categoryoption', models.PositiveSmallIntegerField(blank=True, default=29, null=True, verbose_name='Disaggregation Option')),
                ('measuremethod', models.PositiveSmallIntegerField(blank=True, default=1, null=True, verbose_name='Measure Type')),
                ('numerator_value', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True)),
                ('denominator_value', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True)),
                ('value_received', models.DecimalField(decimal_places=2, default=0.0, max_digits=20, verbose_name='Value Received')),
                ('min_value', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True)),
                ('max_value', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True)),
                ('target_value', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True)),
                ('string_value', models.CharField(blank=True, max_length=200, null=True, verbose_name='String Value')),
                ('start_period', models.CharField(blank=True, max_length=45, null=True, verbose_name='Start Period')),
                ('end_period', models.CharField(blank=True, max_length=45, null=True, verbose_name='End Period')),
                ('period', models.CharField(blank=True, max_length=45, null=True, verbose_name='Period')),
            ],
            options={
                'verbose_name': 'Mapped Fact',
                'verbose_name_plural': 'Mapped Facts',
                'db_table': 'vw_fact_indicator_analytics',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FactsDHIS2_QueryParametersMapped',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Parameter ID')),
                ('pt', models.CharField(max_length=45, verbose_name='Period Type')),
                ('dx', models.CharField(max_length=45, verbose_name='Data Dimension')),
                ('ou', models.CharField(max_length=45, verbose_name='Organisation Unit')),
                ('status', models.PositiveSmallIntegerField(blank=True, default=0, null=True, verbose_name='Status')),
                ('startDate', models.DateField(blank=True, null=True, verbose_name='Start Date')),
                ('endDate', models.DateField(blank=True, max_length=45, null=True, verbose_name='End Date')),
                ('periodname', models.CharField(max_length=100, verbose_name='Period Type')),
                ('period', models.CharField(blank=True, max_length=45, null=True, verbose_name='Period')),
            ],
            options={
                'verbose_name': 'Parameter',
                'verbose_name_plural': 'Show Parameters',
                'db_table': 'vw_dhis2_query_parameters',
                'ordering': ('id',),
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FactsDHIS2_Indicators',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Fact ID')),
                ('indicator', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Indicator ID')),
                ('location', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Country ID')),
                ('datasource', models.PositiveSmallIntegerField(blank=True, default=2, null=True, verbose_name='Datasource ID')),
                ('categoryoption', models.PositiveSmallIntegerField(blank=True, default=29, null=True, verbose_name='Disaggregation Option')),
                ('measuremethod', models.PositiveSmallIntegerField(blank=True, default=1, null=True, verbose_name='Measure Type')),
                ('numerator_value', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True)),
                ('denominator_value', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True)),
                ('value_received', models.DecimalField(decimal_places=2, default=0.0, max_digits=20, verbose_name='Value Received')),
                ('min_value', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True)),
                ('max_value', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True)),
                ('target_value', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True)),
                ('string_value', models.CharField(blank=True, max_length=200, null=True, verbose_name='String Value')),
                ('start_period', models.DateField(blank=True, null=True, verbose_name='Start Period')),
                ('end_period', models.DateField(blank=True, null=True, verbose_name='End Period')),
                ('period', models.CharField(blank=True, max_length=45, null=True, verbose_name='Period')),
            ],
            options={
                'verbose_name': 'Map Fact',
                'verbose_name_plural': 'Map Data-Facts',
                'db_table': 'fact_indicator_analytics',
                'managed': True,
                'unique_together': {('indicator', 'location', 'period')},
            },
        ),
        migrations.CreateModel(
            name='DHIS2_QueryParameters',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('start_period', models.DateField(default=None, verbose_name='Start Date')),
                ('end_period', models.DateField(blank=True, default=None, null=True, verbose_name='End Date')),
                ('period', models.CharField(blank=True, max_length=25, verbose_name='Period')),
                ('status', models.BooleanField(choices=[(1, 'Active'), (0, 'Innactive')], verbose_name='Status')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Created')),
                ('date_lastupdated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date Modified')),
                ('indicator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dhis2metadata.DHIS2Indicators', verbose_name='Data Dimension')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='dhis2metadata.OrganizationUnits', verbose_name='Organisation')),
                ('periodicity', models.OneToOneField(default=None, on_delete=django.db.models.deletion.PROTECT, to='dhis2metadata.PeriodType', verbose_name='Period Type')),
            ],
            options={
                'verbose_name': 'Map Parameter',
                'verbose_name_plural': 'Map Parameters',
                'db_table': 'dhis2_query_parameters',
                'ordering': ('location',),
                'managed': True,
                'unique_together': {('indicator', 'location', 'start_period', 'end_period')},
            },
        ),
    ]