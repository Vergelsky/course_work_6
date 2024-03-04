from django.shortcuts import render

from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from blog.forms import PostForm
from blog.models import Post
from django.urls import reverse_lazy, reverse

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.cache import cache

from mailinger.settings import CACHE_ENABLED


# Create your views here.
class PostCreateView(PermissionRequiredMixin, CreateView):
    model = Post
    permission_required = 'blog.add_post'
    form_class = PostForm
    success_url = reverse_lazy('blog:blog')


class PostListView(ListView):
    model = Post

    def get_queryset(self, *args, **kwargs):
        if CACHE_ENABLED:
            # Проверяем включенность кеша
            key = f'queryset'  # Создаем ключ для хранения
            queryset = cache.get(key)  # Пытаемся получить данные
            if queryset is None:
                # Если данные не были получены из кеша, то выбираем из БД и записываем в кеш
                queryset = super().get_queryset(*args, **kwargs)
                queryset = queryset.filter(is_published=True)
                cache.set(key, queryset)
            return queryset
        else:
            # Если кеш не был подключен, то просто возвращаем результат
            queryset = super().get_queryset(*args, **kwargs)
            queryset = queryset.filter(is_published=True)
            return queryset


class PostDetailView(DetailView):
    model = Post

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return self.object


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'blog/post_update.html'
    model = Post
    permission_required = 'blog.change_blog'
    form_class = PostForm

    def get_success_url(self):
        return reverse('blog:view', args=[self.object.pk])


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    model = Post
    permission_required = 'blog.delete_post'
    success_url = reverse_lazy("blog:blog")


def index(request):
    items_list = Post.objects.all().order_by('datetime')[:3]
    from mailing.models import Mailing
    mailings = Mailing.objects.all().count()
    active_mailings = Mailing.objects.filter(status='started').count()
    from mailing.models import Client
    total_clients = Client.objects.all().count()
    context = {
        'object_list': items_list,
        'mailings_info': {'mailings': mailings, 'active_mailings': active_mailings, 'total_clients': total_clients},
        'title': 'Рассыльщик: Главная',
    }
    return render(request, context=context, template_name='blog/index.html')
