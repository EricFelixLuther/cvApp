# Generated by Django 2.2.12 on 2020-06-03 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cvAppMain', '0013_auto_20200603_1016'),
    ]

    operations = [
        migrations.RenameField(
            model_name='generatedpdf',
            old_name='company',
            new_name='process',
        ),
        migrations.AlterUniqueTogether(
            name='generatedpdf',
            unique_together={('process', 'language')},
        ),
    ]