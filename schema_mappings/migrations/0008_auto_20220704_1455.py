# Generated by Django 3.0.14 on 2022-07-04 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schema_mappings', '0007_auto_20220628_1830'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dhis2_queryparameters',
            options={'managed': True, 'ordering': ('location',), 'verbose_name': 'Parameter', 'verbose_name_plural': '  Map Parameters'},
        ),
    ]