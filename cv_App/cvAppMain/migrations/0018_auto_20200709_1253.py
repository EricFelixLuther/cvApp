# Generated by Django 2.2.12 on 2020-07-09 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cvAppMain', '0017_auto_20200616_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruitmentprocess',
            name='position',
            field=models.CharField(blank=True, default='undisclosed', max_length=64),
        ),
        migrations.AlterField(
            model_name='recruitmentprocess',
            name='recruiting_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cvAppMain.RecruitingCompany'),
        ),
    ]
