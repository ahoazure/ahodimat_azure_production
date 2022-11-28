# Generated by Django 3.0.14 on 2022-08-07 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dctmetadata', '0005_auto_20220704_1455'),
    ]

    operations = [
        migrations.CreateModel(
            name='DCT_Categoryoptions',
            fields=[
                ('id', models.PositiveSmallIntegerField(primary_key=True, serialize=False, verbose_name='Indicator ID')),
                ('code', models.CharField(blank=True, max_length=45, null=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, default='DCT Disaggregation', null=True, verbose_name='Description')),
                ('reference', models.CharField(blank=True, default='DCT', max_length=255, null=True, verbose_name='Disaggregation Options')),
            ],
            options={
                'verbose_name': 'Category Option',
                'verbose_name_plural': 'Category Options',
                'db_table': 'dct_categoryoptions',
                'ordering': ('name',),
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='DCT_Datasource',
            fields=[
                ('id', models.PositiveSmallIntegerField(primary_key=True, serialize=False, verbose_name='Indicator ID')),
                ('code', models.CharField(blank=True, max_length=45, null=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, default='DCT Datasource', null=True, verbose_name='Description')),
                ('reference', models.CharField(blank=True, default='DCT', max_length=255, null=True, verbose_name='Data Source')),
            ],
            options={
                'verbose_name': 'Data Source',
                'verbose_name_plural': 'Data Sources',
                'db_table': 'dct_datasource',
                'ordering': ('name',),
                'managed': True,
            },
        ),
    ]
