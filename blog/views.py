from django.shortcuts import render

from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from blog.forms import PostForm
from blog.models import Post
from django.urls import reverse_lazy, reverse

from django.contrib.auth.mixins import PermissionRequiredMixin


# Create your views here.
class PostCreateView(PermissionRequiredMixin, CreateView):
    model = Post
    permission_required = 'blog.add_post'
    form_class = PostForm
    success_url = reverse_lazy('blog:blog')


class PostListView(ListView):
    model = Post

    def get_queryset(self, *args, **kwargs):
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
    items_list = Post.objects.all()[:3]
    context = {
        'object_list': items_list,
        'title': 'Рассыльщик: Главная'
    }
    return render(request, context=context, template_name='blog/index.html')

