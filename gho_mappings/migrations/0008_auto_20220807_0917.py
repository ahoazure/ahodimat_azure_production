# Generated by Django 3.0.14 on 2022-08-07 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gho_mappings', '0007_auto_20220807_0915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gho_indicatorfacts',
            name='end_period',
            field=models.DateField(blank=True, null=True, verbose_name='End Period'),
        ),
    ]