from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView, name='index'),
    path('lessons/', views.LessonsView, name='lessons'),
    path('homework/', views.HomeWorkView, name='homework'),
    path('logout/', views.LogoutView, name='logout'),
    path('register/', views.RegisterView, name='register'),
    path('login/', views.LoginView, name='login'),
    path('changepw/', views.ChangePasswordView, name='changepw'),
    path('forgotpw/', views.ForgotPasswordView, name='forgotpw'),
]
