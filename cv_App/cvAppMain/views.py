import markdown2

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views import View

from cvAppMain.forms import CompanySelectForm
from cvAppMain.pdf_logic import get_pdf


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
        form = self.form(data=request.POST)
        if form.is_valid():
            context = {"company": form.company}
            for each in form.company.texts.filter(
                    Q(language=form.cleaned_data["language"]) |
                    Q(language__isnull=True)):
                if each.markdown:
                    context[each.text_type.codename] = mark_safe(markdown2.markdown(each.text, extras=["tables"]))
                else:
                    context[each.text_type.codename] = mark_safe(each.text)

            if btn == "get_cv":
                return render(
                    request,
                    form.company.document.name,
                    context=context
                )
            elif btn == "print_cv":
                return get_pdf(form.company, context)
            else:
                return HttpResponse("Bad request!", status=400)
        else:
            return render(
                request,
                template_name=self.template_name,
                context={"form": form}
            )
