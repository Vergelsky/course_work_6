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

from blog import apps
from blog.views import PostCreateView, PostListView, PostDetailView, PostUpdateView, PostDeleteView, index

app_name = apps.BlogConfig.name





urlpatterns = [
    path('', index, name='index'),
    path('new', PostCreateView.as_view(extra_context={'title': "Рассыльщик: Новый пост"}), name='new'),
    path('blog', PostListView.as_view(extra_context={'title': "Рассыльщик: Блог"}), name='blog'),
    path('view/<int:pk>/', PostDetailView.as_view(extra_context={'title': "Рассыльщик: пост"}), name='view'),
    path('edit/<int:pk>/', PostUpdateView.as_view(extra_context={'title': "Рассыльщик: изменить"}), name='edit'),
    path('delete/<int:pk>/', PostDeleteView.as_view(extra_context={'title': "Рассыльщик: удалить"}), name='delete'),
]
