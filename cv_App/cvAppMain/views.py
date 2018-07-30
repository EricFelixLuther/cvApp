# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.template.loader import render_to_string
from django.views import View

from cv_App.cvAppMain.forms import Company_Select_Form_PL, Company_Select_Form_ENG


class CV_Viewer(View):
    select_company = "select_company.html"
    cv_template = None
    form = None

    def get(self, *args, **kwargs):
        return render_to_string(
            template_name="select_company.html",
            context={"form": self.form()}
        )


class CV_pl(View):
    cv_template = "cv_template_pl.html"
    form = Company_Select_Form_PL


class CV_eng(View):
    form = Company_Select_Form_ENG
    cv_template = "cv_template_eng.html"


class CV_export(View):
    pass
