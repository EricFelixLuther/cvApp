from django.contrib import admin
from django.urls import path

from cvAppMain.helpers import cv_viewer_view_name
from cvAppMain.views import CVViewer

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', CVViewer.as_view(), name=cv_viewer_view_name),
]
