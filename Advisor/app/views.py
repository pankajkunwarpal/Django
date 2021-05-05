from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .models import Advisor, Calls
from .forms import LoginForm, UserRegister, SignupForm
from django.views.generic.base import TemplateView
from datetime import datetime
import json

# Create your views here.

class Login(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'app/loginPage.html', {'form': form})

    def post(self, request):
        
        form = LoginForm(request.POST)
        if form.is_valid():
            print("Form's cleaned data {}".format(str(form.cleaned_data)))
            usn, psw = form.cleaned_data['username'], form.cleaned_data['password'] 
            user = authenticate(request, username=usn, password=psw)
            # print(f"User Authentication {user.is_authenticated}")
            
            if user and not user.is_staff:
                login(request, user)
                return redirect('/bookcalls')
                # return HttpResponse('200_OK', request.status)
            
            elif user and user.is_staff:
                login(request, user)
                return redirect('/register')


            else:
                return HttpResponse('400 ', status=400)

        else:
            return HttpResponse("Authentication Failed", status=401)   

        return render(request, 'app/loginPage.html', {'form': LoginForm()})


def Logout(request):
    logout(request)
    return redirect('/login')


class Signup(View):
    
    def get(self, request):
        form = SignupForm()
        print('POPST', request.GET,'user' in request.path) 
        print(form)

        return render(request, 'app/signupPage.html', {'form': form, 'admin': 'admin' in request.path})
    
    def post(self, request):
        print('POPST', request.POST,'user' in request.path)
        form = SignupForm(request.POST)

        if form.is_valid():
            print("User already present or not: ", request.user.username in [_.username for _ in User.objects.all()])
            print(form.cleaned_data)

            User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password1'], email=form.cleaned_data['email'].lower(),
                is_staff='admin' in request.path, first_name=form.cleaned_data['firstname'], last_name=form.cleaned_data['lastname'])

            usn, psw = form.cleaned_data['username'], form.cleaned_data['password1'] 
            user = authenticate(request, username=usn, password=psw)
            
            if user and not user.is_staff:
                login(request, user)

            return redirect('/register')
        
        else:
            return render(request, 'app/signupPage.html', {'form': SignupForm()})


class GetAdvisor(TemplateView):
    template_name = 'app/advisorsPage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['advisors'] = Advisor.objects.all()
        return context


def register(request):
    if request.method == 'POST' and request.user.is_authenticated:
        print('Method POST', request.POST, request.FILES['media'], request.session)
        form = UserRegister(request.POST, request.FILES)
        print(form, '-------\n', request.user.username, request.user.id)
        print(form.is_valid())
        print(form.errors)

        if form.is_valid():
            print(form.cleaned_data)
            Advisor.objects.create(name=form.cleaned_data['name'], media=form.cleaned_data['media'], userid=request.user.id)

            return HttpResponse('200_ok', status=200)

    elif request.method == 'GET' and request.user.is_authenticated:
            form = UserRegister()
            print(form.errors)
    else:
        return redirect('admin/register')
            
    return  render(request, 'app/user-register.html', {'form': form}) 


class BookCall(View):
    def get(self, request):
        
        if not request.user.is_authenticated:
            return redirect('login')
        elif request.user.is_staff:
            return HttpResponse('400 BAD_REQUEST', status=400)

        date = datetime.now().strftime('%Y %B %d %H:%M')

        advisors = [{'Advisor': _, 'date': date} for _ in  Advisor.objects.all()]
        
        return render(request, 'app/bookCallPage.html', {"advisors": advisors, 'user': request.user.username})

    def post(self, request):
        print(request.POST, request.user.id)
        
        if not request.user.is_authenticated:
            return rediect('login')
        elif request.user.is_staff:
            logout(request)
            return HttpResponse('400_BAD REQUEST', status=400)

        Calls.objects.create(userid=request.user.id, advisor=request.POST['id'], 
            date=datetime.strptime(request.POST['date'], '%Y %B %d %H:%M').strftime('%Y-%m-%d %H:%M').__str__())

        return HttpResponse('Booked complete.', status=200)


class BookedCalls(View):
    def get(self, request):
        data = json.dumps([{'Advisor name': Advisor.objects.get(userid=_.advisor).name, 
        'Advisor ID': Advisor.objects.get(userid=_.advisor).userid, 
        'Advisor pic': Advisor.objects.get(userid=_.advisor).media.name, 
        'Booked Time': _.date.__str__(), 'Booked ID': _.userid} for _ in Calls.objects.all()])

        return HttpResponse(data, status=200)
