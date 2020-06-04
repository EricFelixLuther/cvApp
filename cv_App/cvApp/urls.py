from django.contrib import admin
from django.urls import path

from cvAppMain.helpers import cv_viewer_view_name
from cvAppMain.views import CV_Viewer

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get_cv/', CV_Viewer.as_view(), name=cv_viewer_view_name),
    ]
