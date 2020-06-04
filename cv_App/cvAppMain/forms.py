from ckeditor.widgets import CKEditorWidget
from django import forms
from django.utils.translation import gettext as _

from cvAppMain.models import RecruitmentProcess, Language, Text, TextType, ProcessLog, Answer, GeneratedPDF
from cvAppMain.pdf_logic import render_to_pdf


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
        """Make sure there is only one active recruitation process with selected codename"""
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


class AnswerFormset(forms.BaseModelFormSet):
    model = Answer


class GeneratePDFAdminForm(forms.ModelForm):
    class Meta:
        model = GeneratedPDF
        fields = ('process', 'language')
        widgets = {'process': forms.HiddenInput}

    def save(self, *args, **kwargs):
        render_to_pdf(self.instance.process, self.instance.language)
        return self.Meta.model.objects.latest('pk')
