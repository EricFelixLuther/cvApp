from dbtemplates.models import Template
from django.db import models
from simple_history.models import HistoricalRecords


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


class Page(models.Model):
    codename = models.CharField(max_length=64, primary_key=True)
    active = models.BooleanField(default=True)
    document = models.ForeignKey(Template, on_delete=models.CASCADE)
    context = models.ManyToManyField(Text, blank=True)
    notes = models.CharField(max_length=255, blank=True)
    # pictures
    history = HistoricalRecords()

    def __str__(self):
        return self.codename
