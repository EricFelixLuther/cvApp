# Generated by Django 2.2.12 on 2020-05-22 10:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cvAppMain', '0009_auto_20200522_1001'),
    ]

    operations = [
        migrations.CreateModel(
            name='Benefit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='ContactPerson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('phone', models.CharField(max_length=64)),
                ('email', models.CharField(max_length=64)),
                ('notes', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='recruitmentprocess',
            name='fork',
            field=models.CharField(blank=True, max_length=16),
        ),
        migrations.AddField(
            model_name='recruitmentprocess',
            name='notes',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.CreateModel(
            name='RecruitmentAgency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('notes', models.CharField(max_length=255)),
                ('contact_persons', models.ManyToManyField(to='cvAppMain.ContactPerson')),
            ],
        ),
        migrations.CreateModel(
            name='RecruitingCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('location', models.CharField(blank=True, max_length=64)),
                ('notes', models.CharField(blank=True, max_length=128)),
                ('contact_persons', models.ManyToManyField(to='cvAppMain.ContactPerson')),
            ],
        ),
        migrations.CreateModel(
            name='ProcessLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('log', models.CharField(max_length=128)),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cvAppMain.RecruitmentProcess')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalRecruitmentAgency',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('notes', models.CharField(max_length=255)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical recruitment agency',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalRecruitingCompany',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('location', models.CharField(blank=True, max_length=64)),
                ('notes', models.CharField(blank=True, max_length=128)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical recruiting company',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalContactPerson',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('phone', models.CharField(max_length=64)),
                ('email', models.CharField(max_length=64)),
                ('notes', models.CharField(max_length=128)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical contact person',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=64)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cvAppMain.Question')),
            ],
        ),
        migrations.AddField(
            model_name='recruitmentprocess',
            name='benefits',
            field=models.ManyToManyField(to='cvAppMain.Benefit'),
        ),
        migrations.AddField(
            model_name='recruitmentprocess',
            name='my_questions',
            field=models.ManyToManyField(to='cvAppMain.Question'),
        ),
        migrations.AddField(
            model_name='recruitmentprocess',
            name='recruiting_agency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cvAppMain.RecruitmentAgency'),
        ),
        migrations.AddField(
            model_name='recruitmentprocess',
            name='recruiting_company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cvAppMain.RecruitingCompany'),
        ),
        migrations.AddField(
            model_name='recruitmentprocess',
            name='their_answers',
            field=models.ManyToManyField(to='cvAppMain.Answer'),
        ),
        migrations.CreateModel(
            name='GeneratedPDF',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf', models.FileField(upload_to='pdfs/')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cvAppMain.RecruitmentProcess')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cvAppMain.Language')),
            ],
            options={
                'unique_together': {('company', 'language')},
            },
        ),
    ]
