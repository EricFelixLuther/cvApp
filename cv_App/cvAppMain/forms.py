from ckeditor.widgets import CKEditorWidget
from django import forms
from django.utils.translation import gettext as _

from cvAppMain.models import RecruitmentProcess, Language, Text, TextType, ProcessLog, Answer


class CompanySelectForm(forms.ModelForm):
    language = forms.ModelChoiceField(queryset=Language.objects.all(),
                                      required=True)
    class Meta:
        model = RecruitmentProcess
        fields = ["codename"]

    def clean(self):
        if not self.cleaned_data["codename"]:
            self.add_error("codename", "Name not given.")
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

    def clean(self):
        if self.instance.pk and\
                self.cleaned_data['active'] and\
                self.Meta.model.objects.filter(
                    codename=self.cleaned_data['codename'],
                    active=True
                ).exclude(
                    pk=self.instance.pk
                ).first():
            self.add_error('codename', _('There is already an active process with given codename.'))
        return self.cleaned_data


class ProcessLogAdminForm(forms.ModelForm):
    class Meta:
        model = ProcessLog
        fields = '__all__'
        widgets = {'log': forms.Textarea()}
        #widgets = {'log': CKEditorWidget(config_name='default')}


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