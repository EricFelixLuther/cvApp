from django.urls import reverse


cv_viewer_view_name = 'cv_viewer'


def get_cv_url(codename, language, doc_type):
    return (reverse(cv_viewer_view_name) +
            f'?codename={codename}' +
            f'&language={language}' +
            f'&doc_type={doc_type}'
            )
