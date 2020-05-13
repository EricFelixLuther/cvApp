from django import forms
from tinymce.widgets import AdminTinyMCE

from cvAppMain.models import RecruitingCompany, Language, Text, TextType


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


class TextAdminForm(forms.ModelForm):
    text = forms.CharField(widget=AdminTinyMCE())

    class Meta:
        model = Text
        fields = '__all__'


class RecruitingCompanyAdminForm(forms.ModelForm):
    class Meta:
        model = RecruitingCompany
        fields = '__all__'

    # class Media:
    #     css = {'all': ('chosen_v1.8.7/chosen.min.css', 'chosen_v1.8.7/docsupport/prism.css')}
    #     js = (
    #         'jquery.min.js',
    #         'chosen_v1.8.7/chosen.jquery.min.js',
    #         'chosen_v1.8.7/chosen.proto.min.js',
    #         'chosen_v1.8.7/docsupport/prism.js',
    #         'chosen_v1.8.7/docsupport/init.js',
    #         'recruiting_company.js'
    #     )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [
            [text_type.codename, [
                (text.pk, str(text)) for text in Text.objects.filter(text_type=text_type)
            ]] for text_type in TextType.objects.all()
        ]
        self.fields['texts'].choices = choices
