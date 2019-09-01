# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from cvAppMain.models import TextType, Language, Text, RecruitingCompany, Picture

# Register your models here.

admin.site.register((
    TextType,
    Language,
    Text,
    RecruitingCompany,
    Picture
))
