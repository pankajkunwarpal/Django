from django.shortcuts import render, redirect
from .models import Resume
from django.views import View
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden

# Create your views here.

def resume_page(request):
    return render(request, 'resume/resume_page.html', context={'resumes': Resume.objects.all()})

class NewResume(View):

    def get(self, request):
        print(request)
        if not request.user.is_staff:
            return render(request, 'resume/new_resume.html')
        return HttpResponseForbidden(status=403)
    
    def post(self, request):
        print("---", request.POST)
        print()
        if request.user.is_authenticated:
            if not request.user.is_staff:
                Resume.objects.create(author_id=request.user.id, description=request.POST.get('description')).save()
                return redirect('/resumes')
        return HttpResponseForbidden(status=403)
