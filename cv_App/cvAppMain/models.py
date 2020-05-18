import re
from django.db import models
from dbtemplates.models import Template
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
    markdown = models.BooleanField(default=True)
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
    lock_pdf = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.codename = pattern.sub('', self.name).lower()
        return super().save()

    @cached_property
    def text_titles(self):
        return mark_safe(
            ',<br />'.join(
                [str(text) for text in self.texts.order_by('language__lang', 'text_type__codename')]
            )
        )
