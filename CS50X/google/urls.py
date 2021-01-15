from django.urls import path
from .views import HomePage, ImageSearch, AdvanceSearch

urlpatterns = [
    path("", HomePage.as_view(), name="HomePage"),
    path("image", ImageSearch.as_view(), name='ImageSearch'),
    path("advance", AdvanceSearch.as_view(), name='AdvanceSearch'),

]