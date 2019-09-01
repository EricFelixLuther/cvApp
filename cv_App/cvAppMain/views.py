from io import BytesIO

import markdown2
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.views import View
from xhtml2pdf import pisa

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
        btn = request.POST.get("submit", False)
        if btn == "get_cv":
            return self._get_view(request)
        elif btn == "print_cv":
            return self._get_pdf(request)
        else:
            return HttpResponse("Bad request!", status=400)

    def _get_view(self, request):
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

    def _get_pdf(self, request):
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
            html = render_to_string(form.company.document.name, context)
            result = BytesIO()
            pdf = pisa.pisaDocument(html, dest=result)
            if not pdf.err:
                return HttpResponse(result.getvalue(), content_type='application/pdf')
            else:
                return HttpResponse('Error while generating PDF! Sorry!')
        else:
            return render(
                request,
                template_name=self.template_name,
                context={"form": form}
            )
