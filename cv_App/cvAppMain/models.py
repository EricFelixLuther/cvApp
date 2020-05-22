import os
import re
from django.conf import settings
from django.db import models
from dbtemplates.models import Template
from django.dispatch import receiver
from django.http import HttpResponse
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe
from simple_history.models import HistoricalRecords

pattern = re.compile('[\W_]+')


class TextType(models.Model):
    codename = models.CharField(max_length=16)

    def __str__(self):
        return self.codename


class Language(models.Model):
    lang = models.CharField(max_length=32)

    def __str__(self):
        return self.lang


class Text(models.Model):
    title = models.CharField(max_length=64)
    text = models.TextField()
    text_type = models.ForeignKey(TextType, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True, blank=True, default=None)
    history = HistoricalRecords()

    def __str__(self):
        return "%s: %s (%s)" % (
                self.language,
                self.text_type.codename,
                self.title
        )


class Picture(models.Model):
    name = models.CharField(max_length=32)
    pic = models.ImageField(upload_to="static/pics")

    def __str__(self):
        return self.name


class ContactPerson(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    phone = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    notes = models.CharField(max_length=128)
    history = HistoricalRecords()


class RecruitmentAgency(models.Model):
    name = models.CharField(max_length=64)
    contact_persons = models.ManyToManyField(ContactPerson)
    notes = models.CharField(max_length=255)
    history = HistoricalRecords()


class RecruitingCompany(models.Model):
    name = models.CharField(max_length=64)
    contact_persons = models.ManyToManyField(ContactPerson)
    location = models.CharField(max_length=64, blank=True)  # TODO: geolocation
    notes = models.CharField(max_length=128, blank=True)
    history = HistoricalRecords()


class Question(models.Model):
    text = models.CharField(max_length=64)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=64)


class Benefit(models.Model):
    text = models.CharField(max_length=32)


class RecruitmentProcess(models.Model):
    position = models.CharField(max_length=64)
    recruiting_company = models.ForeignKey(RecruitingCompany, on_delete=models.CASCADE)
    recruiting_agency = models.ForeignKey(RecruitmentAgency, on_delete=models.CASCADE, blank=True, null=True)
    codename = models.CharField(max_length=64, blank=True)
    active = models.BooleanField(default=True)
    fork = models.CharField(max_length=16, blank=True)
    my_questions = models.ManyToManyField(Question)
    their_answers = models.ManyToManyField(Answer)
    benefits = models.ManyToManyField(Benefit)
    notes = models.CharField(max_length=255, blank=True)
    document = models.ForeignKey(Template, on_delete=models.CASCADE)
    texts = models.ManyToManyField(Text)
    picture = models.ForeignKey(Picture, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.recruiting_company.name} - {self.position} ({self.fork})'

    def save(self, *args, **kwargs):
        if not self.codename:
            self.codename = pattern.sub('', self.name).lower()
        return super().save()

    @cached_property
    def text_titles(self):
        return mark_safe(
            ',<br />'.join(
                [str(text) for text in self.texts.order_by('language__lang', 'text_type__codename')]
            )
        )


class ProcessLog(models.Model):
    process = models.ForeignKey(RecruitmentProcess, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    log = models.CharField(max_length=128)


class GeneratedPDF(models.Model):
    company = models.ForeignKey(RecruitmentProcess, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='pdfs/')

    class Meta:
        unique_together = ('company', 'language')

    @property
    def pdf_name(self):
        return f'{settings.MEDIA_ROOT}pdfs/{self.company.codename}_{self.language.lang}.pdf'

    def as_response(self):
        with open(self.pdf_name, 'rb') as f:
            return HttpResponse(f, content_type='application/pdf')


@receiver(models.signals.post_delete, sender=GeneratedPDF)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    try:
        os.remove(instance.pdf_name)
    except OSError:
        pass


@receiver(models.signals.pre_save, sender=RecruitmentProcess)
def auto_delete_pdfs_on_update(sender, instance, **kwargs):
    """
    Clear generated PDFs when company is updated.
    """
    if not instance.pk:
        return False

    for each in instance.generatedpdf_set.all():
        each.delete()
