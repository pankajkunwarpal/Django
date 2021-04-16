from django.shortcuts import render, redirect
from django.http import Http404
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.template import loader


# Create your views here.

def index(request):
    return render(request, 'app/homepage.html')


class Login(View):
    
    def get(self, request):
        print("GET===", request.GET)
        return render(request, 'app/loginpage.html')

    def post(self, request):
        usn, psd = request.POST.get('usn'), request.POST.get('psd')
        user = authenticate(request, username=usn, password=psd)

        if (user and user.is_staff):
            login(request, user)
            return redirect('/appointments')

        elif (user and not user.is_staff):
            login(request, user)
            return redirect('/bkslots')

        return HttpResponse(loader.get_template('app/userNotFound.html').render({},request), status=404)


class Logout(View):

    def get(self, request):
        logout(request)
        return redirect('login')


class Singup(View):

    def get(self, request):
        print("GET===", request.GET)
        return render(request, 'app/signuppage.html')

    def post(self, request):
        print("POST===", request.POST)
        
        usn = request.POST.get('usn')
        psd1, psd2 = request.POST.get('psd1'), request.POST.get('psd2') 
        print(psd1, psd2, "password: ", psd1 == psd2, "Username:", User.objects.filter(username__exact=usn))
        fname, lname = request.POST.get('fname'), request.POST.get('lname')
        
        if (psd1 == psd2 and not User.objects.filter(username__exact=usn)):
            User.objects.create_user(username=usn, password=psd1, first_name=fname, last_name=lname)
            print("User {} created succesfully.".format(usn))

        else:
            print("User creation Unsuccesfull.")
            return render(request, 'app/signuppage.html')

        return render(request, 'app/loginpage.html')


