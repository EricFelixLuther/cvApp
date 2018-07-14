# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class BaseData():
    name = "Krzysztof Maciejczuk"
    email = "maciejczuk.krzysztof@gmail.com"
    phone = "796 157 493"
    github = "https://github.com/EricFelixLuther/"


class Summary_Text(models.Model):
    text = models.TextField()


class IT_Tools(models.Model):
    text = models.CharField(max_length=32)


class IT_Tools_List(models.Model):
    it_tool = models.ForeignKey(IT_Tools)
    text = models.CharField(max_length=32)


class IT_Skills(models.Model):
    text = models.CharField(max_length=32)


class Hobbies(models.Model):
    text = models.CharField(max_length=64)


class Languages(models.Model):
    lang = models.CharField(max_length=16)
    level = models.CharField(max_length=3)


class Other_Job_Experience(models.Model):
    name = models.CharField(max_length=32)
    year_from = models.PositiveSmallIntegerField()
    year_to = models.PositiveSmallIntegerField()
    other = models.CharField(max_length=32)


class Job_Experience(models.Model):
    company = models.CharField(max_length=64)
    position = models.CharField(max_length=32)
    start = models.DateField()
    until = models.DateField(blank=True, null=True)


class Job_Details(models.Model):
    detail_type = models.CharField(max_length=14, choices=(("Responsibility", "Responsibility"),
                                                           ("Achievement", "Achievement")))
    text = models.TextField()


class Education(models.Model):
    school = models.CharField(max_length=128)
    start = models.DateField()
    until = models.DateField(blank=True, null=True)
    faculty = models.CharField(max_length=32)
    specialization = models.CharField(max_length=32)
    degree = models.CharField(max_length=16)


class Courses(models.Model):
    title = models.CharField(max_length=64)
    date_from = models.DateField()
    date_until = models.DateField()
    organizer = models.CharField(max_length=32)
    certificate = models.BooleanField()
