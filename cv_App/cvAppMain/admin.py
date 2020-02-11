# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from cvAppMain.forms import TextAdminForm, RecruitingCompanyAdminForm
from cvAppMain.models import TextType, Language, Text, RecruitingCompany, Picture

# Register your models here.

admin.site.register((
    TextType,
    Language,
    Picture
))


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    #form = TextAdminForm
    ordering = ('language__lang', 'text_type__codename', 'markdown')
    list_display = ('title', 'language', 'text_type', 'markdown')
    list_filter = ('language', 'text_type', 'markdown')


@admin.register(RecruitingCompany)
class RecruitingCompany(admin.ModelAdmin):
    form = RecruitingCompanyAdminForm
