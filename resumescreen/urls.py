from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('/resume_extracter', resumeextracter, name='resume_extracter'),
    path('', resume, name='upload_resume'),
    path('result/', predict_resume, name='predict_resume'),
]
