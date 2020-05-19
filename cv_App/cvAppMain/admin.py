# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import re

from ckeditor.widgets import CKEditorWidget
from dbtemplates.admin import TemplateAdmin, TemplateAdminForm
from dbtemplates.models import Template
from django.contrib import admin

from django import forms
from django.utils.translation import ugettext_lazy as _
from simple_history.admin import SimpleHistoryAdmin

from cvAppMain.forms import RecruitingCompanyAdminForm, TextAdminForm
from cvAppMain.models import TextType, Language, Text, RecruitingCompany, Picture


admin.site.register((
    TextType,
    Language,
    Picture
))


@admin.register(Text)
class TextAdmin(SimpleHistoryAdmin):
    form = TextAdminForm
    ordering = ('language__lang', 'text_type__codename', 'title')
    list_display = ('title', 'language', 'text_type')
    list_filter = ('language', 'text_type')
    search_fields = ('title', 'text')
    fields = (('title', 'text_type', 'language'), 'text')


@admin.register(RecruitingCompany)
class RecruitingCompany(admin.ModelAdmin):
    form = RecruitingCompanyAdminForm
    ordering = ('-active', 'name')
    list_display = ('active', 'name', 'codename', 'document', 'picture', 'text_titles')
    list_filter = ('active', 'picture', 'document')
    actions = ['remove_pdfs', 'activate', 'deactivate']
    search_fields = ('name', 'codename')
    list_display_links = ('active', 'name')
    fieldsets = (
        (None, {
            'fields': (('name', 'codename', 'active'), )
        }),
        ('Template settings', {
            'fields': (('document', 'picture'), )
        }),
        (None, {'fields': ('texts', )})
    )

    def remove_pdfs(self, request, queryset):
        removed = []
        for obj in queryset:
            filepath = f'pdfs/{obj.codename}.pdf'
            if os.path.exists(filepath):
                os.remove(filepath)
                removed.append(obj.name)
        if removed:
            message = f'{len(removed)} PDF file{"" if len(removed) == 1 else "s"} removed: {", ".join(removed)}'
        else:
            message = 'No PDF files to remove.'
        self.message_user(request, message)

    remove_pdfs.short_description = "Remove generated PDF files"

    def _set_active(self, request, queryset, active):
        rows_updated = queryset.update(active=active)
        if rows_updated == 1:
            self.message_user(request, f'1 company was {"de" if not active else ""}activated.')
        else:
            self.message_user(request, f'{rows_updated} companies were {"de" if not active else ""}activated.')

    def activate(self, request, queryset):
        self._set_active(request, queryset, True)

    activate.short_description = "Mark recruitation process as active"

    def deactivate(self, request, queryset):
        self._set_active(request, queryset, False)

    deactivate.short_description = "Mark recruitation process as finished"


# Updates on dbtemplates


admin.site.unregister(Template)


class UpdatedDBTemplateAdminForm(TemplateAdminForm):
    extra_screen_css = forms.CharField(widget=forms.Textarea, required=False)
    extra_print_css = forms.CharField(widget=forms.Textarea, required=False)
    extra_js = forms.CharField(widget=forms.Textarea, required=False)
    body = forms.CharField(widget=CKEditorWidget(config_name='advanced'), required=False)

    extra_screen_css_pattern = re.compile("{% block screen_css %}(.*?){% endblock %}", flags=re.DOTALL)
    extra_print_css_pattern = re.compile("{% block print_css %}(.*?){% endblock %}", flags=re.DOTALL)
    extra_js_pattern = re.compile("{% block extra_js %}(.*?){% endblock %}", flags=re.DOTALL)
    body_pattern = re.compile("{% block content %}(.*?){% endblock %}", flags=re.DOTALL)

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
            '{% block screen_css %}' + self.cleaned_data["extra_screen_css"] + '{% endblock %}' +
            '{% block print_css %}' + self.cleaned_data["extra_print_css"] + '{% endblock %}' +
            '{% block extra_js %}' + self.cleaned_data["extra_js"] + '{% endblock %}' +
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
            'fields': ('name', 'extra_screen_css', 'extra_print_css', 'extra_js', 'body'),
            'classes': ('monospace',),
        }),
        (_('Advanced'), {
            'fields': (('sites'),),
        }),
        (_('Date/time'), {
            'fields': (('creation_date', 'last_changed'),),
            'classes': ('collapse',),
        }),
    )
