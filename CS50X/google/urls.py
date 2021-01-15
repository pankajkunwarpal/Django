from django.urls import path
<<<<<<< HEAD
from .views import HomePage, ImageSearch, AdvanceSearch, PianoTiles, FlashCard
=======
from .views import HomePage, ImageSearch, AdvanceSearch
>>>>>>> 7375773 (Google Search Pages.)

urlpatterns = [
    path("", HomePage.as_view(), name="HomePage"),
    path("image", ImageSearch.as_view(), name='ImageSearch'),
    path("advance", AdvanceSearch.as_view(), name='AdvanceSearch'),
<<<<<<< HEAD
    path('piano_tiles', PianoTiles.as_view()),
    path('flashcard', FlashCard.as_view()),
=======
>>>>>>> 7375773 (Google Search Pages.)

]