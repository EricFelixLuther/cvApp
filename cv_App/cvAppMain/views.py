import markdown2
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views import View

from cvAppMain.forms import CompanySelectForm
from cvAppMain.models import BaseData

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
            context = {
                "company": form.company,
                "base_data": BaseData
            }
            for each in form.company.texts.filter(language=form.cleaned_data["language"]):
                if each.markdown:
                    context[each.text_type.codename] = mark_safe(markdown2.markdown(each.text, extras=["tables"]))
                else:
                    context[each.text_type.codename] = mark_safe(each.text)
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
