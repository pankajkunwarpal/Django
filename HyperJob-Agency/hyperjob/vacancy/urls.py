from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth.views import LogoutView
from .views import MainPage, VacancyPage, LoginPage, SignupPage, HomePage, NewVacancy, logout_view

urlpatterns = [
    path("", MainPage.as_view(), name='main_page'),
    path('vacancies', VacancyPage.as_view(), name='vacancy_page'),
    path('login', LoginPage.as_view(), name='login_page'),
    path('signup', SignupPage.as_view(), name='sign_page'),
    path('accounts/profile/', RedirectView.as_view(url='/home')),
    path('home', HomePage.as_view(), name='HomePage'),
    path('vacancy/new', NewVacancy.as_view(), name='new_vacancy'),
    path('_vacancy/new', RedirectView.as_view(url='/vacancy/new')),
    path('logout', LogoutView.as_view(), name='logout'),
]
