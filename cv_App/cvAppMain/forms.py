from ckeditor.widgets import CKEditorWidget
from django import forms

from cvAppMain.models import RecruitmentProcess, Language, Text, TextType, ProcessLog, Answer


class CompanySelectForm(forms.ModelForm):
    language = forms.ModelChoiceField(queryset=Language.objects.all(),
                                      required=True)
    class Meta:
        model = RecruitmentProcess
        fields = ["codename"]

    def clean(self):
        if not self.cleaned_data["name"]:
            self.add_error("name", "Name not given.")
        else:
            self.company = self.Meta.model.objects.filter(name=self.cleaned_data['name']).first()
            if not self.company:
                self.add_error("name", "Your company did not contact me for recruitment purposes.")
            else:
                if not self.company.active:
                    self.add_error("name",
                                   "Your company does not have access to my CV anymore. "
                                   "If you wish to see it, please contact me again.")
        return self.cleaned_data


class TextAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget(config_name='advanced'))

    class Meta:
        model = Text
        fields = '__all__'


class RecruitmentProcessAdminForm(forms.ModelForm):
    class Meta:
        model = RecruitmentProcess
        fields = '__all__'
        widgets = {'notes': CKEditorWidget(config_name='default')}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [
            [text_type.codename, [
                (text.pk, str(text)) for text in Text.objects.filter(text_type=text_type)
            ]] for text_type in TextType.objects.all()
        ]
        self.fields['texts'].choices = choices


class ProcessLogAdminForm(forms.ModelForm):
    class Meta:
        model = ProcessLog
        fields = '__all__'
        widgets = {'log': forms.Textarea()}
        #widgets = {'log': CKEditorWidget(config_name='default')}

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if self.instance and self.instance.pk:
    #         self.fields['log'].widget = forms.HiddenInput()
    #     else:
    #         self.fields['log'].widget = CKEditorWidget(config_name='default')


class AnswerFormset(forms.BaseModelFormSet):
    model = Answer
    #
    # def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
    #              queryset=None, *, initial=None, **kwargs):
    #     self.queryset = queryset
    #     self.initial_extra = initial
    #     super().__init__(**{'data': data, 'files': files, 'auto_id': auto_id, 'prefix': prefix, **kwargs})
    #
    # def get_queryset(self):
    #     return super().get_queryset()