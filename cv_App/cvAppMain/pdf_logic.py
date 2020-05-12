import logging
import os

from django.http import HttpResponse
from django.template.loader import render_to_string


logger = logging.getLogger('debug')


def get_pdf(company, context):
    try:
        if company.lock_pdf:
            # Find previously generated file
            with open(f'pdfs/{company.codename}.pdf', 'rb') as f:
                response = HttpResponse(f, content_type='application/pdf')
        else:
            response = render_to_pdf(company, context)
    except FileNotFoundError:  # If none was generated, generate it
        response = render_to_pdf(company, context)

    return response

def render_to_pdf(company, context):
    try:  # Render HTML into a file, try generating it
        html = render_to_string(company.document.name, context)
        with open(f'{company.codename}.html', 'w') as f:
            f.write(str(html))

        os.system(f'wkhtmltopdf {company.codename}.html pdfs/{company.codename}.pdf')
        os.remove(f'{company.codename}.html')  # Remove HTML, it's redundant now

        with open(f'pdfs/{company.codename}.pdf', 'rb') as f:
            return HttpResponse(f, content_type='application/pdf')

    except Exception as e:
        logger.error(e)
        return HttpResponse('Something went wrong while generating PDF! Sorry!')
