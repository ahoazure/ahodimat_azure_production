# Generated by Django 3.0.14 on 2022-08-07 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dctmetadata', '0007_auto_20220807_1137'),
        ('gho_mappings', '0012_auto_20220807_1157'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='factsghodct_indicators',
            unique_together={('indicator', 'location', 'categoryoption', 'period')},
        ),
    ]