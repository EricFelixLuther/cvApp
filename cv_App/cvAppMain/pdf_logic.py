import logging
import os

from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from django.utils.safestring import mark_safe

from cvAppMain.helpers import get_cv_url
from cvAppMain.models import GeneratedPDF

logger = logging.getLogger('django')


def make_context(process, language):
    """Makes a context for CV generating"""
    context = {"process": process}
    for each in process.texts.filter(
            Q(language=language) |
            Q(language__isnull=True)):
        context[each.text_type.codename] = mark_safe(each.text)
    return context


def get_pdf(process, language):
    """Gets a cached PDF from DB or calls generating a new one"""
    saved_file = process.generatedpdf_set.filter(language=language).first()
    if saved_file:
        return saved_file.as_response()
    else:
        return render_to_pdf(process, language)


def render_to_pdf(process, language):
    """Uses WKHTMLTOPDF to generate a PDF from URL.
    This function requires PROTOCOL and HOST settings to be set."""
    temp_pdf = f'pdfs/{process.codename}_{language.lang}.pdf'

    try:
        os.system(f'wkhtmltopdf "{settings.PROTOCOL}{settings.HOST}{get_cv_url(process.codename, language, "html")}" {temp_pdf}')
    except Exception as e:
        logger.error("Error while generating PDF: " + str(e))

    try:
        saved_pdf = GeneratedPDF.objects.create(process=process, language=language, pdf=temp_pdf)
        return saved_pdf.as_response()
    except Exception as e:
        logger.error("Error while saving and returning PDF: " + str(e))
        return HttpResponse('Something went wrong while generating PDF! Sorry!')
