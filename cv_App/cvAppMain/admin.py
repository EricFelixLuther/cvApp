# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from cvAppMain.models import TextTypes, Languages, Texts, RecruitingCompany

# Register your models here.

admin.site.register((TextTypes, Languages, Texts, RecruitingCompany))
