# Generated by Django 2.2.5 on 2020-01-25 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_authentication', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='company_detail',
            new_name='company_details',
        ),
    ]