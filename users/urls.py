"""
URL configuration for mailinger project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from users import apps
from users.views import RegisterView, confirm_email, ProfileView

app_name = apps.UsersConfig.name

urlpatterns = [
    path('',
         LoginView.as_view(extra_context={'title': "Рассыльщик: Авторизация"},
                           template_name='users/login.html'),
         name='login'),
    path('register', RegisterView.as_view(extra_context={'title': "Рассыльщик: Регистрация"}), name='register'),
    path('confirm_email/<token>/', confirm_email, name='confirm_email'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('logout', LogoutView.as_view(next_page='.'), name='logout'),

]
