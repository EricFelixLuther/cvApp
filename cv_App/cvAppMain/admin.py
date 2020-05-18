# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from cvAppMain.forms import RecruitingCompanyAdminForm
from cvAppMain.models import TextType, Language, Text, RecruitingCompany, Picture


admin.site.register((
    TextType,
    Language,
    Picture
))


@admin.register(Text)
class TextAdmin(SimpleHistoryAdmin):
    #form = TextAdminForm
    ordering = ('language__lang', 'text_type__codename', 'title')
    list_display = ('title', 'language', 'text_type', 'markdown')
    list_filter = ('language', 'text_type', 'markdown')
    search_fields = ('title', 'text')
    fields = (('title', 'text_type', 'language', 'markdown'), 'text')


@admin.register(RecruitingCompany)
class RecruitingCompany(admin.ModelAdmin):
    form = RecruitingCompanyAdminForm
    ordering = ('-active', 'name')
    list_display = ('active', 'name', 'codename', 'document', 'picture', 'lock_pdf', 'text_titles')
    list_filter = ('active', 'lock_pdf', 'picture', 'document')
    actions = ['remove_pdfs', 'activate', 'deactivate', 'lock', 'unlock']
    search_fields = ('name', 'codename')
    list_display_links = ('active', 'name')
    fieldsets = (
        (None, {
            'fields': (('name', 'codename'), )
        }),
        ('Controls', {
            'fields': (('active', 'lock_pdf'), )
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

    def _set_lock_pdfs(self, request, queryset, lock):
        rows_updated = queryset.update(lock_pdf=lock)
        if rows_updated == 1:
            self.message_user(request, f'1 company\'s PDF was {"un" if not lock else ""}locked.')
        else:
            self.message_user(request, f'{rows_updated} companies\' PDFs were {"un" if not lock else ""}locked.')

    def lock(self, request, queryset):
        self._set_lock_pdfs(request, queryset, True)

    lock.short_description = 'Lock PDF generation'

    def unlock(self, request, queryset):
        self._set_lock_pdfs(request, queryset, False)

    unlock.short_description = 'Unlock PDF generation'
