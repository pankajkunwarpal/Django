from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import LoginView, SingupView, HomeView, logout_view

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path("login", LoginView.as_view(), name='login'),
    path("signup", SingupView.as_view(), name='signup'),
    path('home', HomeView.as_view(), name='home'),
    path('logout', logout_view, name='logout'),
]
