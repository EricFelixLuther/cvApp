from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from cvAppMain.forms import CompanySelectForm
from cvAppMain.pdf_logic import get_pdf, make_context


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
            if btn == "get_cv":
                return render(
                    request,
                    form.company.document.name,
                    context=make_context(form.company, form.cleaned_data["language"])
                )
            elif btn == "print_cv":
                return get_pdf(form.company, form.cleaned_data["language"])
            else:
                return HttpResponse("Bad request!", status=400)
        else:
            return render(
                request,
                template_name=self.template_name,
                context={"form": form}
            )
