# Generated by Django 2.2.12 on 2020-05-13 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cvAppMain', '0005_auto_20200205_1639'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='text',
            name='markdown',
        ),
    ]