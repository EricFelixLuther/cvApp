# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from cvApp.cvAppMain.models import Summary_Text, IT_Tools, , IT_Tools_List,\
    IT_Skills, Hobbies, Languages, Other_Job_Experience, Job_Experience,\
    Job_Details, Education, Courses, Company

admin.register((Summary_Text, IT_Tools, IT_Tools_List, IT_Skills, Hobbies, Languages, Other_Job_Experience,
                Job_Experience, Job_Details, Education, Courses, Company))
