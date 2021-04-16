from django.urls import path
from .views import index, Login, Singup, Logout
from .appointments import BookedAppoints, MakingAppoints, MakingBookings

urlpatterns = [
    path("", index, name='home'),
    path('login', Login.as_view(), name='login'),
    path('signup', Singup.as_view(), name='signup'),
    path('logout', Logout.as_view(), name='logout'),
    path('appointments', BookedAppoints.as_view(), name='appoints'),
    path('bkslots', MakingAppoints.as_view(), name='userpage'),
    path('makebookings', MakingBookings.as_view(), name='makebooking'),

]