from django.shortcuts import render, redirect
from django.views import View

# Create your views here.
class HomePage(View):

    def get(self, request, *args, **kargs):
        print("Request type", request)
        return render(request, 'google/homePage.html')


class ImageSearch(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'google/imagePage.html')


class AdvanceSearch(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'google/advancePage.html')
