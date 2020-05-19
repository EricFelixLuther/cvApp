import os
import re
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


class RecruitingCompany(models.Model):
    name = models.CharField(max_length=64)
    codename = models.CharField(max_length=64, blank=True)
    active = models.BooleanField(default=True)
    document = models.ForeignKey(Template, on_delete=models.CASCADE)
    texts = models.ManyToManyField(Text)
    picture = models.ForeignKey(Picture, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

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


class GeneratedPDF(models.Model):
    company = models.ForeignKey(RecruitingCompany, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='pdfs/')

    class Meta:
        unique_together = ('company', 'language')

    @property
    def pdf_name(self):
        return f'pdfs/{self.company.codename}_{self.language.lang}.pdf'

    def as_response(self):
        with open(self.pdf_name, 'rb') as f:
            return HttpResponse(f, content_type='application/pdf')


@receiver(models.signals.post_delete, sender=GeneratedPDF)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    try:
        os.remove(instance.pdf_name)
    except OSError:
        pass


@receiver(models.signals.pre_save, sender=RecruitingCompany)
def auto_delete_pdfs_on_update(sender, instance, **kwargs):
    """
    Clear generated PDFs when company is updated.
    """
    if not instance.pk:
        return False

    for each in instance.generatedpdf_set.all():
        each.delete()
