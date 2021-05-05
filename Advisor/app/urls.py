from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import register, Login, Signup, GetAdvisor, BookCall, Logout, BookedCalls

urlpatterns = [
    path('register', register, name='user-register'),
    path('login', Login.as_view(), name='loginPage'),
    path('user/register', Signup.as_view(), name='signupPage'),
    path('admin/register', Signup.as_view(),name='registerPage'), 
    path('advisors', GetAdvisor.as_view(), name='advisors'),
    path('bookcalls', BookCall.as_view(), name='bookCalls'),
    path('logout', Logout, name='logout'),
    path('bookedcalls', BookedCalls.as_view(), name='bookedcalls'),
]
