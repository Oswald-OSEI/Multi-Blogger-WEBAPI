from django.urls import path 
from django.contrib.auth import views as auth_views
from .import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('register/', views.UserRegistration, name = 'registration'), 
    path('login/',views.UserLogin, name = 'login'), 
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('view profile/', views.viewProfile, name = 'user profile'), 
    path('edit profile/', views.editProfile, name = 'update profile'), 
]