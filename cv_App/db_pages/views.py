from django.http import Http404
from django.shortcuts import render
from django.views import View


class DBHTMLViewer(View):
    """Allows viewing saved dbtemplates as flatpages.
    Advantage of this is that flatpages do not allow Django Template tags.
    This way user can create templates, extend, include, use templatetags, etc.
    In form of security, only templates without .html ending can be displayed.
    This distinguishes viewable pages from raw HTML templates."""

    def get(self, request, page, *args, **kwargs):
        if page.lower().endswith('.html'):
            return Http404('404: Page not found!')
        else:
            pass
