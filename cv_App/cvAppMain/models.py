import os
import re

from django.db import models
from dbtemplates.models import Template
from django.dispatch import receiver
from django.http import HttpResponse
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe
from django.utils.timezone import now
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
    phone = models.CharField(max_length=64, blank=True)
    email = models.EmailField(max_length=128, blank=True)
    linkedin = models.URLField(max_length=256, blank=True)
    notes = models.CharField(max_length=128, blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ('last_name', 'first_name')


class RecruitmentAgency(models.Model):
    name = models.CharField(max_length=64)
    contact_persons = models.ManyToManyField(ContactPerson, blank=True)
    notes = models.CharField(max_length=255, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', )


class RecruitingCompany(models.Model):
    name = models.CharField(max_length=64)
    contact_persons = models.ManyToManyField(ContactPerson, blank=True)
    location = models.CharField(max_length=64, blank=True)  # TODO: geolocation
    notes = models.CharField(max_length=128, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.CharField(max_length=64)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('text', )


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=128, blank=True)
    process = models.ForeignKey('RecruitmentProcess', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.question.text}: {self.text}'


class Benefit(models.Model):
    text = models.CharField(max_length=32)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('text', )


class RecruitmentProcess(models.Model):
    position = models.CharField(max_length=64)
    recruiting_company = models.ForeignKey(RecruitingCompany, on_delete=models.CASCADE,
                                           null=True)
    recruiting_agency = models.ForeignKey(RecruitmentAgency, on_delete=models.CASCADE,
                                          blank=True, null=True)
    codename = models.CharField(max_length=64, blank=True)
    active = models.BooleanField(default=True)
    fork = models.CharField(max_length=32, blank=True)
    benefits = models.ManyToManyField(Benefit, blank=True)
    notes = models.CharField(max_length=255, blank=True)
    document = models.ForeignKey(Template, on_delete=models.CASCADE, blank=True)
    texts = models.ManyToManyField(Text, blank=True)
    picture = models.ForeignKey(Picture, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.recruiting_company} - {self.position} ({self.fork})'

    def save(self, *args, **kwargs):
        if not self.codename:
            self.codename = pattern.sub('', self.recruiting_company.name).lower()
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
    timestamp = models.DateTimeField(blank=True, default=now)
    log = models.CharField(max_length=128)

    class Meta:
        ordering = ('-timestamp',)

class GeneratedPDF(models.Model):
    process = models.ForeignKey(RecruitmentProcess, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='pdfs/')

    class Meta:
        unique_together = ('process', 'language')

    def as_response(self):
        return HttpResponse(self.pdf, content_type='application/pdf')

    def __str__(self):
        return f'{self.process} / {self.language}'


@receiver(models.signals.post_delete, sender=GeneratedPDF)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    try:
        os.remove(instance.pdf.path)
    except OSError:
        pass


@receiver(models.signals.post_delete, sender=RecruitmentProcess)
def auto_delete_pdfs_on_delete(sender, instance, **kwargs):
    """
    Clear generated PDFs when recruiting process is deleted.
    """
    for pdf in instance.generatedpdf_set.all():
        pdf.delete()
