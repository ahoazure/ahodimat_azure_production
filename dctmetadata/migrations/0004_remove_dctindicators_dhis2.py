# Generated by Django 3.0.14 on 2022-06-28 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dctmetadata', '0003_auto_20220628_1637'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dctindicators',
            name='dhis2',
        ),
    ]