from django.urls import path
from .views import resume_page, NewResume


urlpatterns = [
    path('resumes', resume_page, name='resumes'),
    path('resume/new', NewResume.as_view(), name='new_resume')
]
