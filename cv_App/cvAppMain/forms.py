from django import forms

from cvAppMain.models import RecruitingCompany, Language


class CompanySelectForm(forms.ModelForm):
    language = forms.ModelChoiceField(queryset=Language.objects.all(),
                                      required=True)
    class Meta:
        model = RecruitingCompany
        fields = ["name"]

    def clean(self):
        if not self.cleaned_data["name"]:
            self.add_error("name", "Name not given.")
        else:
            self.company = self.Meta.model.objects.filter(name=self.cleaned_data['name']).first()
            if not self.company:
                self.add_error("name", "Your company did not contact me for recruitment purposes.")
            else:
                if not self.company.active:
                    self.add_error("name", "Your company does not have access to my CV anymore. If you wish to see it, again, please contact me again.")
        return self.cleaned_data
