from django.shortcuts import render, redirect
from django.views import View

# Create your views here.
class HomePage(View):

    def get(self, request, *args, **kargs):
<<<<<<< HEAD

        print("Request type -- ", self.request.GET)
=======
        print("Request type", request)
>>>>>>> 7375773 (Google Search Pages.)
        return render(request, 'google/homePage.html')


class ImageSearch(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'google/imagePage.html')


class AdvanceSearch(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'google/advancePage.html')
<<<<<<< HEAD

class PianoTiles(View):
    def get(self, request):
        return render(request, 'google/pianoTiles.html')


class FlashCard(View):
    def get(self, request):
        return render(request, 'google/flashcard.html')

        
=======
>>>>>>> 7375773 (Google Search Pages.)
