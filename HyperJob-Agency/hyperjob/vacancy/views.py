from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.views import View
from .models import Vacancy
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
import random

# Create your views here.
def logout_view(request):
    logout(request)
    return redirect('/login')


class NewVacancy(View):
    def get(self, request):
        print(request)
        if request.user.is_authenticated and request.user.is_staff:
            return render(request, 'vacancy/new_vacancy.html')
        return HttpResponseForbidden(status=403)

    def post(self, request):
        print(request)
        if request.user.is_authenticated and request.user.is_staff:
            Vacancy(description=request.POST.get('vacancy'), author_id=request.user.id).save()
            return redirect('/vacancies')
        return HttpResponseForbidden(status=403)
    

class VacancyPage(View):
    def get(self, request):
        print(request)
        print(Vacancy.objects.all())        
        context = {"vacancies": Vacancy.objects.all()}
        return render(request, 'vacancy/vacancies.html', context=context)


class MainPage(TemplateView):
    template_name = 'vacancy/main_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context


# class LoginPage(View):
#     def get(self, request):
#         print("GET Method")
#         return render(request, 'vacancy/login.html')

#     def post(self, request, *args, **kwargs):
#         print("Post method")
#         print(request.POST)
#         print(*User.objects.all(), sep='\n')
#         return redirect('/home')


class LoginPage(LoginView):
    # form_class = AuthenticationForm()
    # # authentication_form = AuthenticationForm
    redirect_authenticated_user = True
    template_name = 'vacancy/login.html'

    # def get(self, request, *args, **kwargs):
    #     print(request)
    #     print('Authenticated',  request.user.is_authenticated)
    #     return render(request, 'vacancy/login.html')

#     def post(self, request, *args, **kwargs):
#         print(request)
#         return redirect('/home')

class SignupPage(CreateView):
    form_class = UserCreationForm
    success_url = 'login'
    template_name = 'vacancy/signup.html'

    # def post(self, request, *args, **kwargs):
    #     print(request)
    #     return redirect('/login')


class HomePage(View):
    def get(self, request):
        print(request)
        print(request.user, request.user.id)
        context = {"User": request.user.username,
                   'is_staff': request.user.is_staff}
        return render(request, "vacancy/home_page.html", context=context)
    def post(self, request):
        print(request)
        print("INSIDE POST VACANCY")

