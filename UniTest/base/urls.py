from django.urls import path
from . import views

urlpatterns = [
    path('',          views.home,          name = 'index'),
    path('login/',    views.loginUser,     name = 'login'),
    path('register/', views.registerPage,  name = 'register'),
    path('logout/',   views.logoutUser,    name = 'logout'),
    path('home/',     views.homePage,      name = 'homePage'),
]