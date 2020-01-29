import os
import markdown2
import logging

from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.views import View

from cvAppMain.forms import CompanySelectForm
from cvAppMain.models import BaseData


logger = logging.getLogger('debug')


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
            context = {
                "company": form.company,
                "base_data": BaseData
            }
            for each in form.company.texts.filter(language=form.cleaned_data["language"]):
                if each.markdown:
                    context[each.text_type.codename] = mark_safe(markdown2.markdown(each.text, extras=["tables"]))
                else:
                    context[each.text_type.codename] = mark_safe(each.text)

            if btn == "get_cv":
                return self._get_view(request, form, context)
            elif btn == "print_cv":
                return self._get_pdf(request, form, context)
            else:
                return HttpResponse("Bad request!", status=400)
        else:
            return render(
                request,
                template_name=self.template_name,
                context={"form": form}
            )

    def _get_view(self, request, form, context):
        return render(
            request,
            form.company.document.name,
            context=context
        )

    def _get_pdf(self, request, form, context):
        try:
            # Find previously generated file
            f = open(f'pdfs/{form.company.codename}.pdf', 'rb')
        except IOError:  # If none was generated
            try:  # Render HTML into a file, try generating it
                html = render_to_string(form.company.document.name, context)
                with open(f'{form.company.codename}.html', 'w') as f:
                    f.write(str(html))

                os.system(f'wkhtmltopdf {form.company.codename}.html pdfs/{form.company.codename}.pdf')
                os.remove(f'{form.company.codename}.html')  # Remove HTML, it's redundant now

                with open(f'pdfs/{form.company.codename}.pdf', 'rb') as f:
                    return HttpResponse(f, content_type='application/pdf')

            except Exception as e:
                logger.error(e)
                return HttpResponse('Something went wrong while generating PDF! Sorry!')
        # Return previously generated PDF
        return HttpResponse(f, content_type='application/pdf')
