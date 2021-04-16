from django.urls import path
from .views import HomePage, ImageSearch, AdvanceSearch, PianoTiles, FlashCard

urlpatterns = [
    path("", HomePage.as_view(), name="HomePage"),
    path("image", ImageSearch.as_view(), name='ImageSearch'),
    path("advance", AdvanceSearch.as_view(), name='AdvanceSearch'),
    path('piano_tiles', PianoTiles.as_view()),
    path('flashcard', FlashCard.as_view()),

]