# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from dbtemplates.models import Template

# Create your models here.


class BaseData:
    name = "Krzysztof Maciejczuk"
    email = "maciejczuk.krzysztof@gmail.com"
    phone = "796 157 493"
    github = "https://github.com/EricFelixLuther/"


class TextTypes(models.Model):
    codename = models.CharField(max_length=16)

    def __str__(self):
        return self.codename


class Languages(models.Model):
    lang = models.CharField(max_length=32)

    def __str__(self):
        return self.lang


class Texts(models.Model):
    text = models.TextField()
    text_type = models.ForeignKey(TextTypes, on_delete=models.CASCADE)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE)

    def __str__(self):
        return self.text_type.codename + " " + self.text[:20]


class RecruitingCompany(models.Model):
    name = models.CharField(max_length=64)
    codename = models.CharField(max_length=64, blank=True)
    active = models.BooleanField(default=True)
    document = models.ForeignKey(Template, on_delete=models.CASCADE)
    texts = models.ManyToManyField(Texts)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.codename = self.name.replace(" ", "").lower()
        return super().save()
