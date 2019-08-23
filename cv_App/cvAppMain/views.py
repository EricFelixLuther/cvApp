# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View

from cvAppMain.forms import CompanySelectForm


class CV_Viewer(View):
    template_name = "select_company.html"
    form = CompanySelectForm

    def get(self, request, *args, **kwargs):
        return render(
            request,
            template_name=self.template_name,
            context={"form": self.form()}
        )

    def post(self, request, *args, **kwargs):
        form = self.form(data=request.POST)
        if form.is_valid():
            context = {}
            for each in form.company.texts.filter(language=form.cleaned_data["language"]):
                context[each.text_type.codename] = each.text
            return render(
                request,
                form.company.document.name,
                context=context
            )
        else:
            return render(
                request,
                template_name=self.template_name,
                context={"form": form}
            )


class CV_export(View):
    pass
