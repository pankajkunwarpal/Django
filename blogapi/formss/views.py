from django.utils import timezone
from django.http.response import JsonResponse, HttpResponse 
from django.shortcuts import render, redirect
from django.forms import modelform_factory, modelformset_factory
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist


from .models import Person, PersonDetails, Blog, Blogs
from .forms import PersonDetailForm, PersonForm, BlogForm, LoginForm


from datetime import datetime, timedelta


# Create your views here.

def username(request, username):
    if request.method == "GET":
        try:
            return HttpResponse(User.objects.get(username=username).id)
        except ObjectDoesNotExist:
            return HttpResponse("No id for this username", status=401)

class SignupView(View):
    def get(self, request):
        # form1 = modelformset_factory(PersonDetails, fields=('gender', 'dob'))
        # form2 = modelformset_factory(Person, fields=['person', 'detail'])
        form = PersonForm()
        return render(request, 'formss/form.html', {'form': form, 'request': request})

    def post(self, request):
        form = PersonForm(request.POST)
        

        if form.is_valid():
            User.objects.create_user(
                username = form.cleaned_data['username'],
                first_name = form.cleaned_data['firstname'],
                last_name = form.cleaned_data['lastname'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'], 
                
                is_staff = True,               
            ).groups.set(Group.objects.all())
            user = authenticate(
                request, username=form.cleaned_data['username'], 
                password=form.cleaned_data['password1']
            )
            print(user)
            if user.is_authenticated:
                login(request, user)   
                
                return redirect(request.path + 'details')
      
        return render(request, 'formss/form.html', {'form': form, 'request': request})



class PersonDetailsFormView(View):
    def get(self, request):
        if request.user.is_anonymous:
            return redirect('login')
        form = PersonDetailForm()
        
        return render(request, 'formss/form.html', {'form': form, 'request': request})

    def post(self, request):
        age = (datetime.now().date() - datetime.strptime(request.POST['dob'], '%Y/%m/%d').date()).days//365
        form = PersonDetailForm({"gender": request.POST['gender'], 'dob': datetime.strptime(request.POST['dob'], '%Y/%m/%d').date(),
        'age': age})

        if form.is_valid():
            person = PersonDetails.objects.create(gender=form.cleaned_data['gender'], dob=form.cleaned_data['dob'], age=age)
            Person.objects.create(person=User.objects.get(id=request.user.id), detail=person)
            return redirect('blog')
        return render(request, 'formss/form.html', {'form': form, 'request': request})



class BlogView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        form = BlogForm()
        return render(request, 'formss/form.html', {'form': form, 'request': request})

    def post(self, request):
        if request.user.is_anonymous:
            return redirect('login')
        
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = Blog.objects.create(title=form.cleaned_data['title'], blog=form.cleaned_data['blog'])
            Blogs.objects.create(blog=blog, person=Person.objects.get(
                person__id=request.user.id), date_created=timezone.now)
            # blogs = [_ for _ in Blogs.objects.get(person__id=request.user.id).blog]
            # return render(request, 'formss/blog.html', {'blogs': blogs})
            return redirect('blogs')
        else: 
            return HttpResponse('invalid form data')




class BlogsView(View):
    def get(self, request):
         return render(request, 'formss/blogs.html', 
            {
                'blogs': [{'title': _.blog.title, 'blog': _.blog.blog
            } for _ in Blogs.objects.filter(person__person__id=request.user.id)], 'request': request})



class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            try:
                if PersonDetails.objects.get(person__person__username=request.user):
                    return redirect('blog')
            except ObjectDoesNotExist:
                return redirect('/signup/details') 

        form = LoginForm()
        return render(request, 'formss/form.html', {'form': form, 'request': request})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                if request.user.is_authenticated:
                    try:
                        if PersonDetails.objects.get(person__person__username=request.user):
                            return redirect('blog')
                    except ObjectDoesNotExist:
                        return redirect('/signup/details') 
                
        return render(request, 'formss/form.html', {'form': form, 'request': request})
        


def logout_view(request):
    logout(request)
    return redirect('login')

def home(request):
    if request.user.is_authenticated:
        return redirect('blogs')
    return  render(request, 'formss/homepage.html')