# -*- coding: utf-8 -*-

from django import forms

from cvAppMain.models import RecruitingCompany, Languages


class CompanySelectForm(forms.ModelForm):
    language = forms.ModelChoiceField(queryset=Languages.objects.all(),
                                      required=True)
    class Meta:
        model = RecruitingCompany
        fields = ["name"]
        widgets = {"name": forms.TextInput}

    def clean(self):
        if not self.cleaned_data["name"]:
            self.add_error("name", "Name not given.")
        else:
            codename = self.cleaned_data["name"].replace(" ", "").lower()
            self.company = self.Meta.model.objects.filter(codename=codename).first()
            if not self.company:
                self.add_error("name", "Your company did not contact me for recruitment purposes.")
            else:
                if not self.company.active:
                    self.add_error("name", "Your company does not have access to my CV anymore. If you wish to see it, again, please contact me again.")
        return self.cleaned_data
