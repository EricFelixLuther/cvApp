from django.conf.urls import url
from django.contrib import admin

from cvAppMain.views import CV_Viewer

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', CV_Viewer.as_view(), name='cv_viewer'),
]
