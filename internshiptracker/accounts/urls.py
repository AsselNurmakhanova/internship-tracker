from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('home/', views.home, name='home_page'),
    path('login/', views.login_page, name='login'), 
    path('signup/', views.signup_page, name='signup'), 
    path('main/', views.main_page, name='main'),
]