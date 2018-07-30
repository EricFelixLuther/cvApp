# -*- coding: utf-8 -*-

from django import forms

from cv_App.cvAppMain.models import Company


class Company_Select_Abstract(forms.ModelForm):
    missing_error = ''
    not_found_error = ''

    class Meta:
        abstract = True

    def clean(self):
        if not self.cleaned_data:
            self.add_error("name", self.missing_error)
        else:
            try:
                self.company = self.Meta.model.objects.get(name=self.cleaned_data["name"])
            except self.Meta.model.DoesNotExist:
                self.add_error("name", self.not_found_error)


class Company_Select_Form_PL(Company_Select_Abstract):
    missing_error = 'Nie podano nazwy firmy'
    not_found_error = 'Nie znaleziono firmy o tej nazwie'

    class Meta:
        model = Company
        fields = ["name"]
        widgets = {"name": forms.CharField(label="Proszę wprowadzić nazwę firmy")}


class Company_Select_Form_ENG(Company_Select_Abstract):
    missing_error = 'Company name was not given'
    not_found_error = 'Company with given name has not been found'

    class Meta:
        model = Company
        fields = ["name"]
        widgets = {"name": forms.CharField(label="Please, enter company's name")}
