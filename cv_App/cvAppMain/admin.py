# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from ckeditor.widgets import CKEditorWidget
from dbtemplates.admin import TemplateAdmin, TemplateAdminForm
from dbtemplates.models import Template
from django.contrib import admin

from django import forms
from django.utils.translation import ugettext_lazy as _
from django_ace import AceWidget
from simple_history.admin import SimpleHistoryAdmin

from cvAppMain.forms import RecruitmentProcessAdminForm, TextAdminForm, ProcessLogAdminForm, AnswerFormset
from cvAppMain.models import TextType, Language, Text, RecruitmentProcess, Picture, GeneratedPDF, ContactPerson, \
    RecruitmentAgency, RecruitingCompany, Question, Answer, Benefit, ProcessLog

admin.site.register((
    TextType,
    Language,
    Picture,
    ContactPerson,
    RecruitmentAgency,
    RecruitingCompany,
    Question,
    Benefit,
    Answer
))


@admin.register(Text)
class TextAdmin(SimpleHistoryAdmin):
    form = TextAdminForm
    ordering = ('language__lang', 'text_type__codename', 'title')
    list_display = ('title', 'language', 'text_type')
    list_filter = ('language', 'text_type')
    search_fields = ('title', 'text')
    fields = (('title', 'text_type', 'language'), 'text')


class ProcessLogAdminInline(admin.StackedInline):
    model = ProcessLog
    extra = 1
    form = ProcessLogAdminForm
    template = 'log_admin_form.html'


class AnswerAdminInline(admin.StackedInline):
    model = RecruitmentProcess.their_answers.through
    extra = 0
    verbose_name = 'Recruiter answers'
    #
    # def get_formset(self, request, obj=None, **kwargs):
    #     queryset = obj.their_answers.all()
    #     initial = obj.my_questions.exclude(
    #         id__in=queryset.values_list('pk', flat=True)
    #     ).values()
    #     return super().get_formset(request, obj,
    #                                queryset=queryset,
    #                                initial=initial
    #                                )


@admin.register(RecruitmentProcess)
class RecruitmentProcessAdmin(admin.ModelAdmin):
    form = RecruitmentProcessAdminForm
    ordering = ('-active', 'recruiting_company__name')
    list_display = (
        'active', '__str__', 'codename', 'recruiting_agency', 'document', 'picture')
    list_filter = ('active', 'picture', 'document', 'recruiting_company')
    actions = ['remove_pdfs', 'activate', 'deactivate']
    search_fields = (
        'position', 'codename', 'recruiting_company__name', 'recruiting_agency__name',
        'fork', 'my_questions__text', 'their_answers__text', 'benefits__text', 'notes',
        'texts__title', 'texts__text'
    )
    list_display_links = ('active', '__str__')
    fieldsets = (
        ('Basic', {
            'fields': (('position', 'recruiting_company', 'recruiting_agency'), )
        }),
        ('Additional', {
            'fields': (('active', 'fork', 'codename'), ('benefits', 'my_questions'),
                       'notes')
        }),
        ('CV Template Settings', {
            'fields': (('document', 'picture'), 'texts')
        })
    )

    inlines = (ProcessLogAdminInline, AnswerAdminInline)

    def remove_pdfs(self, request, queryset):
        files = 0
        for each in GeneratedPDF.objects.filter(company__in=queryset):
            each.delete()
            files += 1
        if files == 1:
            self.message_user(request, '1 cached file was deleted.')
        elif files > 1:
            self.message_user(request, f'{files} cached files were deleted.')
        else:
            self.message_user(request, 'No cached files were deleted.')
    remove_pdfs.short_description = "Remove generated PDF files"

    def _set_active(self, request, queryset, active):
        rows_updated = queryset.update(active=active)
        if rows_updated == 1:
            self.message_user(
                request,
                f'1 company was {"de" if not active else ""}activated.'
            )
        else:
            self.message_user(
                request,
                f'{rows_updated} companies were {"de" if not active else ""}activated.'
            )

    def activate(self, request, queryset):
        self._set_active(request, queryset, True)
    activate.short_description = 'Mark recruitation process as active'

    def deactivate(self, request, queryset):
        self._set_active(request, queryset, False)
    deactivate.short_description = 'Mark recruitation process as finished'


# Updates on dbtemplates


admin.site.unregister(Template)


def get_ace_css_widget():
    return AceWidget(mode='css', theme='twilight', width='580px',
        height='350px', tabsize=2)


def get_ace_js_widget():
    return AceWidget(mode='javascript', theme='twilight', width='1200px',
                     height='500px', tabsize=2)


class UpdatedDBTemplateAdminForm(TemplateAdminForm):
    body = forms.CharField(widget=CKEditorWidget(config_name='advanced'), required=False)
    extra_screen_css = forms.CharField(widget=get_ace_css_widget(), required=False)
    extra_print_css = forms.CharField(widget=get_ace_css_widget(), required=False)
    extra_js = forms.CharField(widget=get_ace_js_widget(), required=False)

    extra_screen_css_pattern = re.compile('{% block screen_css %}(.*?){% endblock %}', flags=re.DOTALL)
    extra_print_css_pattern = re.compile('{% block print_css %}(.*?){% endblock %}', flags=re.DOTALL)
    extra_js_pattern = re.compile('{% block extra_js %}(.*?){% endblock %}', flags=re.DOTALL)
    body_pattern = re.compile('{% block content %}(.*?){% endblock %}', flags=re.DOTALL)

    class Meta:
        model = Template
        fields = ('name', 'sites', 'creation_date', 'last_changed')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            content = str(self.instance.content)
            extra_screen_css_content = self.extra_screen_css_pattern.findall(content)
            extra_print_css_content = re.findall(self.extra_print_css_pattern, content)
            extra_js_content = re.findall(self.extra_js_pattern, content)
            body_content = re.findall(self.body_pattern, self.instance.content)

            if extra_screen_css_content:
                self.initial['extra_screen_css'] = extra_screen_css_content[0]
            if extra_print_css_content:
                self.initial['extra_print_css'] = extra_print_css_content[0]
            if extra_js_content:
                self.initial['extra_js'] = extra_js_content[0]
            if body_content:
                self.initial['body'] = body_content[0]

    def save(self, commit=True):
        if not self.cleaned_data.get('body'):
            return super().save(commit)

        self.instance.content = (
            '{% extends "main.html" %}' +
            '{% block screen_css %}' + self.cleaned_data['extra_screen_css'] + '{% endblock %}' +
            '{% block print_css %}' + self.cleaned_data['extra_print_css'] + '{% endblock %}' +
            '{% block extra_js %}' + self.cleaned_data['extra_js'] + '{% endblock %}' +
            '{% block content %}' + self.cleaned_data['body'] + '{% endblock %}'
        )
        self.instance.save()
        return self.instance

    def save_m2m(self, *args, **kwargs):
        """Django throws error if this is not present, even though it's not needed."""
        pass


@admin.register(Template)
class UpdatedDBTemplate(TemplateAdmin):
    form = UpdatedDBTemplateAdminForm
    fieldsets = (
        (None, {
            'fields': ('name', 'body'),
            'classes': ('monospace',),
        }),
        ('CSS', {
            'fields': (('extra_screen_css', 'extra_print_css'),),
            'classes': ('monospace', 'collapse'),
        }),
        ('JavaScript', {
            'fields': ('extra_js',),
            'classes': ('monospace', 'collapse'),
        }),
        (_('Advanced'), {
            'fields': (('sites'),),
            'classes': ('collapse',),
        }),
        (_('Date/time'), {
            'fields': (('creation_date', 'last_changed'),),
            'classes': ('collapse',),
        }),
    )
