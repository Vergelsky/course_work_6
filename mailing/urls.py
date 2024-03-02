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
from mailing.views.mailing_views import MailingListView, MailingCreateView, MailingDetailView, MailingUpdateView, \
    MailingDeleteView
from mailing.views.letter_views import LetterListView, LetterCreateView, LetterDetailView, LetterUpdateView, \
    LetterDeleteView
from mailing.views.log_views import LogListView
app_name = apps.MailingConfig.name

urlpatterns = [
    # Клиенты
    path('new_client', ClientCreateView.as_view(extra_context={'title': "Рассыльщик: Новый клиент"}),
         name='new_client'),
    path('client/<int:pk>', ClientDetailView.as_view(extra_context={'title': "Рассыльщик: Клиент"}),
         name='client'),
    path('', ClientListView.as_view(extra_context={'title': "Рассыльщик: Список клиентов"}),
         name='client_list'),
    path('client_update/<int:pk>', ClientUpdateView.as_view(extra_context={'title': "Рассыльщик: Изменить клиента"}),
         name='client_update'),
    path('client_confirm_delete/<int:pk>',
         ClientDeleteView.as_view(extra_context={'title': "Рассыльщик: Удалить клиента"}),
         name='client_confirm_delete'),
    # Рассылки
    path('new_mailing', MailingCreateView.as_view(extra_context={'title': "Рассыльщик: Новая рассылка"}),
         name='new_mailing'),
    path('mailing/<int:pk>', MailingDetailView.as_view(extra_context={'title': "Рассыльщик: Рассылка"}),
         name='mailing'),
    path('mailings', MailingListView.as_view(extra_context={'title': "Рассыльщик: Список рассылок"}),
         name='mailing_list'),
    path('mailing_update/<int:pk>', MailingUpdateView.as_view(extra_context={'title': "Рассыльщик: Изменить рассылку"}),
         name='mailing_update'),
    path('mailing_confirm_delete/<int:pk>',
         MailingDeleteView.as_view(extra_context={'title': "Рассыльщик: Удалить рассылку"}),
         name='mailing_confirm_delete'),
    # Письма
    path('new_letter', LetterCreateView.as_view(extra_context={'title': "Рассыльщик: Новое письмо"}),
         name='new_letter'),
    path('letter/<int:pk>', LetterDetailView.as_view(extra_context={'title': "Рассыльщик: Письмо"}),
         name='letter'),
    path('letters', LetterListView.as_view(extra_context={'title': "Рассыльщик: Список писем"}),
         name='letter_list'),
    path('letter_update/<int:pk>', LetterUpdateView.as_view(extra_context={'title': "Рассыльщик: Изменить письмо"}),
         name='letter_update'),
    path('letter_confirm_delete/<int:pk>',
         LetterDeleteView.as_view(extra_context={'title': "Рассыльщик: Удалить письмо"}),
         name='letter_confirm_delete'),

    # Логи
    path('logs', LogListView.as_view(extra_context={'title': "Рассыльщик: Логи"}),
         name='log_list'),
]
