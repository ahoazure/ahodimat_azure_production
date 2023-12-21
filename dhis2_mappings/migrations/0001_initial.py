# Generated by Django 3.0.14 on 2023-12-20 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dhis2metadata', '0001_initial'),
        ('dctmetadata', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DHIS2DCT_IndicatorsMapped',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Indicator ID')),
                ('dct_indicator_name', models.CharField(max_length=45, verbose_name='DCT Indicator Name')),
                ('afrocode', models.CharField(max_length=45, verbose_name='DCT Indicator Code')),
                ('dhis2_indicator', models.CharField(max_length=100, verbose_name='DHIS2 Indicator Name')),
                ('dhis_indicator_uid', models.CharField(blank=True, max_length=45, null=True, verbose_name='DHIS2 Indicator ID')),
                ('dct_indicator_id', models.PositiveIntegerField(verbose_name='DCT Indicator ID')),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Mapped Indicators',
                'db_table': 'vw_dhis2_dct_mapped_indicators',
                'ordering': ('dct_indicator_name',),
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DHIS2DCT_LocationsMapped',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Location ID')),
                ('location_name', models.CharField(max_length=45, verbose_name='Location Name')),
                ('country_code', models.CharField(max_length=45, verbose_name='Location Code')),
                ('locationlevel', models.PositiveSmallIntegerField(blank=True, default=0, null=True, verbose_name='Location Level')),
                ('dhis_uid', models.CharField(max_length=100, verbose_name='DHIS2 UID')),
                ('dhis_code', models.CharField(blank=True, max_length=45, null=True, verbose_name='DHIS2 CODE')),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Mapped Countries',
                'db_table': 'vw_dhis2_mapped_dct_locations',
                'ordering': ('location_name',),
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
                ('status', models.CharField(blank=True, max_length=45, null=True, verbose_name='Status')),
            ],
            options={
                'verbose_name': 'Mapped Fact',
                'verbose_name_plural': ' Mapped Facts',
                'db_table': 'vw_dhis2_indicator_facts',
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
                ('dct_indicator', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Mapped Indicator')),
                ('period', models.CharField(blank=True, max_length=45, null=True, verbose_name='Period')),
            ],
            options={
                'verbose_name': 'Parameter',
                'verbose_name_plural': ' Mapped Parameters',
                'db_table': 'vw_dhis2_mapped_parameters',
                'ordering': ('id',),
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FactsDHIS2_Indicators',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Fact ID')),
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
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10, verbose_name='Status')),
                ('categoryoption', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='dctmetadata.DCT_Categoryoptions', verbose_name='Disaggregation Option')),
                ('datasource', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='dctmetadata.DCT_Datasource', verbose_name='Datasource ID')),
                ('indicator', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='dctmetadata.DCTIndicators', verbose_name='Indicator ID')),
                ('location', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='dctmetadata.DCTLocations', verbose_name='Country ID')),
                ('measuremethod', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='dctmetadata.DCT_Measuretype', verbose_name='Measure Type')),
            ],
            options={
                'verbose_name': 'Fact',
                'verbose_name_plural': '  Fetched Facts',
                'db_table': 'dhis2_indicator_facts',
                'managed': True,
                'unique_together': {('indicator', 'location', 'period')},
            },
        ),
        migrations.CreateModel(
            name='DHIS2DCT_MapOrgunitLocations',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Location ID')),
                ('location', models.OneToOneField(default=None, on_delete=django.db.models.deletion.PROTECT, to='dctmetadata.DCTLocations', verbose_name='DCT Related Location')),
                ('orgunit', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='dhis2metadata.OrganizationUnits', verbose_name='DHIS2 Organisation Unit')),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Map Countries',
                'db_table': 'dhis2_dct_mapped_orgunits',
                'ordering': ('location',),
                'managed': True,
                'unique_together': {('orgunit', 'location')},
            },
        ),
        migrations.CreateModel(
            name='DHIS2_QueryParameters',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('start_period', models.DateField(default=None, verbose_name='Start Date')),
                ('end_period', models.DateField(blank=True, default=None, null=True, verbose_name='End Date')),
                ('status', models.BooleanField(choices=[(1, 'Active'), (0, 'Innactive')], verbose_name='Status')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Created')),
                ('date_lastupdated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date Modified')),
                ('dctindicator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dctmetadata.DCTIndicators', verbose_name='DCT Indicator')),
                ('indicator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dhis2metadata.DHIS2Indicators', verbose_name='DHI2 Indicator')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='dhis2metadata.OrganizationUnits', verbose_name='Organisation')),
                ('periodicity', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='dhis2metadata.PeriodType', verbose_name='Period Type')),
            ],
            options={
                'verbose_name': 'Parameter',
                'verbose_name_plural': '  Map Parameters',
                'db_table': 'dhis2_query_parameters',
                'ordering': ('location',),
                'managed': True,
                'unique_together': {('dctindicator', 'indicator', 'location', 'periodicity')},
            },
        ),
    ]