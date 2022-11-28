# Generated by Django 3.0.14 on 2022-06-28 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dctmetadata', '0002_auto_20220628_1232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dctindicators',
            name='description',
            field=models.TextField(blank=True, default='DCT indicator', null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='dctindicators',
            name='reference',
            field=models.CharField(blank=True, default='DCT', max_length=255, null=True, verbose_name='Indicator Source'),
        ),
    ]