from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

import rest_framework
from rest_framework import response

from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication, JWTTokenUserAuthentication
from rest_framework.response import Response
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import token_refresh

from datetime import datetime as dt
import jwt
from django.conf import settings

from .models import UserDetails

# Create your views here.

def get_user_token(user):
    refresh = RefreshToken.for_user(user)
    print({'token':refresh})
    return {
        'access': refresh.access_token,
        'refresh': refresh
    }


def logout_view(request):
    logout(request)
    response = redirect('/login')
    response.set_cookie('access', '', expires=1)
    response.set_cookie('refresh', '', expires=1)
    return response


class LoginView(View):
    
    def get(self, request):
        return render(request, 'app/login.html')

    def post(self, request):
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['pswd'])
        print(user)

        if user:
            login(request, user)
            refresh = get_user_token(user)
            
            response = redirect('/home')
            response.set_cookie('access', refresh['access'], expires=300)
            response.set_cookie('refresh', refresh['refresh'], expires=24*60*60)

            return response

        return render(request, 'app/login.html', {'error': 'Incorrect username or password'})



class SingupView(View):
    
    def get(self, request):
        return render(request, 'app/signup.html')

    def post(self, request):
        print(request.POST)
        print(User.objects.filter(username=request.POST.get('username')).count())
        print(bool(User.objects.filter(username=request.POST.get('username')).count()))

        if User.objects.filter(username=request.POST.get('username')).count():

            return render(request, 'app/signup.html', {'error': 'Username already taken'})

        UserDetails.objects.create(user=User.objects.create_user(username=request.POST.get('username'),
                        email=request.POST.get('email'), password=request.POST.get('password')),
                        address=request.POST.get('address'))    
        
        return redirect('/login')
        


def get_token(token: str):
    return JWTAuthentication().get_validated_token(token)

def get_user(token):
    return JWTAuthentication.get_user(get_token(token))

def validate_token(token):
    if token:
        return False
    token = get_token(token)
    a_exp = token.get('exp')
    now = dt.now().timestamp()
    
    return (now - a_exp) < 300

def validate_refresh_and_new_token(token):

    try:
        token_details = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        if token_details['token_type'] == 'refresh':
            return RefreshToken(token).access_token

    except jwt.InvalidSignatureError as e:
        return e
    except jwt.ExpiredSignatureError as e:
        return e 

class HomeView(View):

    def get(self, request):
        cookies = request.COOKIES

        if cookies.get('refresh'):
            users = UserDetails.objects.all()
            
            if cookies.get('access'):
                return render(request, 'app/home.html', {'users': users})
                
            access = validate_refresh_and_new_token(cookies.get('refresh'))
            print(access)

            response = render(request, 'app/home.html', {'users': users})
            response.set_cookie('access', access, expires=300)    
            return response

        return redirect('/login')

    def post(self, request):
        print(request.POST)

        if request.POST.get('delete'):
            ob = UserDetails.objects.get(id=request.POST.get('id'))
            User.objects.get(id=ob.user.id).delete()
            ob.delete()
        
        if request.POST.get('edit'):
            ob = UserDetails.objects.get(id=int(request.POST.get('userid')))
            if request.POST.get('address'):
                ob.address = request.POST.get('address')
            if request.POST.get('email'):
                user = User.objects.get(id=ob.user.id)
                user.email = request.POST.get('email')
                user.save()
            ob.save()

        return render(request, 'app/home.html', {'users': UserDetails.objects.all()})

