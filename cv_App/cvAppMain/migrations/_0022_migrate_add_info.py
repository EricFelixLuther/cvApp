# Generated by Django 2.2.13 on 2021-05-14 19:19

from django.db import migrations


def forwards(apps, schema_editor):
    Answer = apps.get_model('cvAppMain', 'Answer')
    Question = apps.get_model('cvAppMain', 'Question')
    Benefit = apps.get_model('cvAppMain', 'Benefit')
    ProcessLog = apps.get_model('cvAppMain', 'ProcessLog')
    RecruitmentProcess = apps.get_model('cvAppMain', 'RecruitmentProcess')
    NewAnswer = apps.get_model('additional_process_info', 'Answer')
    NewQuestion = apps.get_model('additional_process_info', 'Question')
    NewBenefit = apps.get_model('additional_process_info', 'Benefit')
    NewProcessLog = apps.get_model('additional_process_info', 'ProcessLog')

    for each in Answer.objects.all().select_related('question'):
        NewAnswer.objects.create(
            question=NewQuestion.objects.get_or_create(text=each.question.text),
            text=each.text,
            process=each.process
        )

    for each in ProcessLog.objects.all().select_related('recruitment_process'):
        NewProcessLog.objects.create(
            process=each.process,
            timestamp=each.timestamp,
            log=each.log
        )

    for each in RecruitmentProcess.objects.all().prefetch_related('benefits'):
        for each_benefit in each.benefits.all():
            benefit = NewBenefit.objects.get_or_create(text=each_benefit.text)
            each.new_benefits.add(benefit)


class Migration(migrations.Migration):

    dependencies = [
        ('cvAppMain', '0021_migrate_cv_contents'),
        ('additional_process_info', '0001_initial')
    ]

    operations = [
        migrations.RunPython(forwards),
    ]