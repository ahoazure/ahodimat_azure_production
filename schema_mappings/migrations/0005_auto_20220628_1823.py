# Generated by Django 3.0.14 on 2022-06-28 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dhis2metadata', '0005_auto_20220628_1818'),
        ('dctmetadata', '0004_remove_dctindicators_dhis2'),
        ('schema_mappings', '0004_auto_20220628_1818'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='dhis2_queryparameters',
            unique_together={('dctindicator', 'indicator', 'location', 'periodicity')},
        ),
    ]
