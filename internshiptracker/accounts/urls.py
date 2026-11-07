from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('home/', views.home, name='home_page'),
    path('login/', views.login_page, name='login'), 
    path('signup/', views.signup_page, name='signup'), 
    path('main/', views.main_page, name='main'),
    path('internships/<int:pk>/edit/', views.edit_internship, name='edit_internship'),
    path('internships/<int:pk>/delete/', views.delete_internship, name='delete_internship'),
    path('profile/', views.edit_profile, name='edit_profile'),
    path('logout/', views.logout_page, name='logout'),
]