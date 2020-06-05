from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from cvAppMain.forms import CompanySelectForm
from cvAppMain.helpers import get_cv_url
from cvAppMain.models import RecruitmentProcess, Language
from cvAppMain.pdf_logic import get_pdf, make_context


class CV_Viewer(View):
    template_name = "select_company.html"
    form = CompanySelectForm

    def get(self, request, *args, **kwargs):
        if request.GET:
            return self._get_cv(request)
        else:
            return render(
                request,
                template_name=self.template_name,
                context={"form": self.form()}
            )

    def _get_cv(self, request):
        codename = request.GET.get('codename')
        language = request.GET.get('language')
        doc_type = request.GET.get('doc_type', 'html')

        process = RecruitmentProcess.objects.filter(
            codename=codename,
            active=True
        ).first()
        language = get_object_or_404(Language, lang=language)
        if process:
            if doc_type == 'html':
                return render(
                    request,
                    process.document.name,
                    context=make_context(process, language)
                )
            elif doc_type == 'pdf':
                return get_pdf(process, language)
            else:
                return HttpResponse("Unknown document type requested.", status=400)
        else:
            other_processes = RecruitmentProcess.objects.filter(codename=codename)
            if other_processes:
                return HttpResponse(
                    'This CV is no longer available to this company. If you wish to view it again '
                    'please, contact me on LinkedIn, or on e-mail: krzysztof at maciejczuk dot pl',
                    status=403
                )
            else:
                return HttpResponse(
                    'Your company did not contact me regarding recruitment. '
                    'Please, contact me on LinkedIn, or on e-mail: krzysztof at maciejczuk dot pl',
                    status=404
                )

    def post(self, request, *args, **kwargs):
        btn = request.POST.get("submit", False)
        form = self.form(data=request.POST)
        if form.is_valid():
            return redirect(
                get_cv_url(
                    form.cleaned_data["codename"],
                    form.cleaned_data["language"],
                    btn
                )
            )
        else:
            return render(
                request,
                template_name=self.template_name,
                context={"form": form}
            )
