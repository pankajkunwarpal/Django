from django.urls import path, include
from .views import (
    SignupView, PersonDetailsFormView, BlogView,
    LoginView, logout_view, BlogsView, home, username)
    
from .apis import (BlogsSerializerView, BlogSerializerView, PersonSerializerView,
    UserSerializerView, CreateUserSerializerView, PersonDetailSerializerView)

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView 
# from rest_framework.authtoken import views

# routers = routers.DefaultRouter()
# routers.register(r'api/blog/', BlogSerializerView)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('signup/details/', PersonDetailsFormView.as_view(), name='signup-details'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('blogs/', BlogsView.as_view(), name='blogs'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    # path("", include(routers.urls)),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    # path('api-token/', AuthToken.as_view()),
    path('api/blogs/', BlogsSerializerView.as_view(), name='blogs-api'),
    path('api/blog/', BlogSerializerView.as_view(), name='blog-api'),
    path('api/person/details/', PersonSerializerView.as_view(), name='api-person-details'),
    path('api/register/person/', CreateUserSerializerView.as_view(), name='api-register-person'),
    path('api/register/detail/', PersonDetailSerializerView.as_view(), name='api-register-detail'),
    path('api/person/name/', UserSerializerView.as_view(), name='api-person-name'),
    path('api/person/detail/', PersonDetailSerializerView.as_view(), name='api-person-detail'),
    path('username/<str:username>', username),
    path('', home, name='home'),
]