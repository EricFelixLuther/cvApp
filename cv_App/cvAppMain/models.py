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
    text_eng = models.TextField()


class IT_Tools(models.Model):
    text = models.CharField(max_length=32)
    text_eng = models.CharField(max_length=32)


class IT_Tools_List(models.Model):
    it_tool = models.ForeignKey(IT_Tools)
    text = models.CharField(max_length=32)
    text_eng = models.CharField(max_length=32)


class IT_Skills(models.Model):
    text = models.CharField(max_length=32)
    text_eng = models.CharField(max_length=32)


class Hobbies(models.Model):
    text = models.CharField(max_length=64)
    text_eng = models.CharField(max_length=64)


class Languages(models.Model):
    lang = models.CharField(max_length=16)
    level = models.CharField(max_length=3)
    lang_eng = models.CharField(max_length=16)


class Other_Job_Experience(models.Model):
    name = models.CharField(max_length=32)
    year_from = models.PositiveSmallIntegerField()
    year_to = models.PositiveSmallIntegerField()
    other = models.CharField(max_length=32)
    name_eng = models.CharField(max_length=32)
    other_eng = models.CharField(max_length=32)


class Job_Experience(models.Model):
    company = models.CharField(max_length=64)
    position = models.CharField(max_length=32)
    start = models.DateField()
    until = models.DateField(blank=True, null=True)
    company_eng = models.CharField(max_length=64)
    position_eng = models.CharField(max_length=32)


class Job_Details(models.Model):
    detail_type = models.CharField(max_length=14, choices=(("Responsibility", "Responsibility"),
                                                           ("Achievement", "Achievement")))
    text = models.TextField()
    text_eng = models.TextField()


class Education(models.Model):
    school = models.CharField(max_length=128)
    start = models.DateField()
    until = models.DateField(blank=True, null=True)
    faculty = models.CharField(max_length=32)
    specialization = models.CharField(max_length=32)
    degree = models.CharField(max_length=16)
    school_eng = models.CharField(max_length=128)
    faculty_eng = models.CharField(max_length=32)
    specialization_eng = models.CharField(max_length=32)
    degree_eng = models.CharField(max_length=16)


class Courses(models.Model):
    title = models.CharField(max_length=64)
    date_from = models.DateField()
    date_until = models.DateField()
    organizer = models.CharField(max_length=32)
    certificate = models.BooleanField()
    title_eng = models.CharField(max_length=64)
    organizer_eng = models.CharField(max_length=32)


class Company(models.Model):
    name = models.CharField(max_length=32)
    summary = models.ForeignKey(Summary_Text)
    it_tools = models.ManyToManyField(IT_Tools)
    it_skills = models.ManyToManyField(IT_Skills)
    hobbies = models.ManyToManyField(Hobbies)
    languages = models.ManyToManyField(Languages)
    other_jobs = models.ManyToManyField(Other_Job_Experience)
    job_experience = models.ManyToManyField(Job_Experience)
    education = models.ManyToManyField(Education)
    courses = models.ManyToManyField(Courses)
