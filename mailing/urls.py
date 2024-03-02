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
from mailing import apps
from mailing.views.client_views import ClientListView, ClientCreateView, ClientDetailView, ClientUpdateView, \
    ClientDeleteView

app_name = apps.MailingConfig.name

urlpatterns = [
    path('new_client', ClientCreateView.as_view(extra_context={'title': "Рассыльщик: Новый клиент"}),
         name='new_client'),
    path('client/<int:pk>', ClientDetailView.as_view(extra_context={'title': "Рассыльщик: Клиент"}),
         name='client'),
    path('', ClientListView.as_view(extra_context={'title': "Рассыльщик: Список клиентов"}),
         name='client_list'),
    path('client_update/<int:pk>', ClientUpdateView.as_view(extra_context={'title': "Рассыльщик: Список клиентов"}),
         name='client_update'),
    path('client_confirm_delete/<int:pk>', ClientDeleteView.as_view(extra_context={'title': "Рассыльщик: Список клиентов"}),
         name='client_confirm_delete'),
]
