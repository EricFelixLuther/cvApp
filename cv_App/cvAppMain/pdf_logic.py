import logging
import os
from datetime import datetime

from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from cvAppMain.models import GeneratedPDF

logger = logging.getLogger('debug')


def make_context(company, language):
    """Makes a context for CV generating"""
    context = {"company": company}
    for each in company.texts.filter(
            Q(language=language) |
            Q(language__isnull=True)):
        context[each.text_type.codename] = mark_safe(each.text)
    return context


def get_pdf(company, language):
    """Gets a cached PDF from DB or calls generating a new one"""
    saved_file = company.generatedpdf_set.filter(language=language).first()
    if saved_file:
        return saved_file.as_response()
    else:
        return render_to_pdf(company, language)


def render_to_pdf(company, language):
    """Uses WKHTMLTOPDF to generate a PDF from an HTML file."""
    microseconds = datetime.now().microsecond
    temp_html = f'{microseconds}.html'
    temp_pdf = company.pdf_name

    try:
        # First, create an HTML file
        html = render_to_string(company.document.name, make_context(company, language))
        # and save it into the local storage
        with open(temp_html, 'w') as f:
            f.write(str(html))
        # Launch WKHTMLtoPDF to generate PDF
        os.system(f'wkhtmltopdf {temp_html} {temp_pdf}')
        # Save PDF into DB
        saved_pdf = GeneratedPDF.objects.create(company=company, language=language, pdf=temp_pdf)
        # Remove both files as they're no longer necessary
        os.remove(temp_html)
        os.remove(temp_pdf)

        return saved_pdf.as_response()
    except Exception as e:
        os.remove(temp_html)
        os.remove(temp_pdf)
        logger.error(e)
        return HttpResponse('Something went wrong while generating PDF! Sorry!')
