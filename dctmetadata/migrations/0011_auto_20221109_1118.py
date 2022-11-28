# Generated by Django 3.0.14 on 2022-11-09 11:18

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dctmetadata', '0010_remove_dctlocations_dhis2orgunit'),
    ]

    operations = [
        migrations.CreateModel(
            name='DCTConfigs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dct_url', models.CharField(max_length=200, validators=[django.core.validators.RegexValidator(message="Valid URL:'https://abc.com; or http://abc.com:8000'", regex='https?:\\/\\/(?:w{1,3}\\.)?[^\\s.]+(?:\\.[a-z]+)*(?::\\d+)?(?![^<]*(?:<\\/\\w+>|\\/?>))')], verbose_name='DCT URL')),
                ('dct_user', models.CharField(max_length=200, verbose_name='Username')),
                ('dct_passkey', models.CharField(max_length=300, verbose_name='Password')),
                ('status', models.BooleanField(choices=[(1, 'Active'), (0, 'Innactive')], default=1, verbose_name='Status')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='DHIS2 User/Email')),
            ],
            options={
                'verbose_name': 'DCT Setup',
                'verbose_name_plural': 'DCT Settings',
                'db_table': 'ahodct_configs',
                'managed': True,
            },
        ),
        migrations.AlterField(
            model_name='dct_urlendpointpath',
            name='url',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dctmetadata.DCTConfigs', verbose_name='DCT URL'),
        ),
    ]