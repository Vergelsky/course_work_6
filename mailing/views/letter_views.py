from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse

from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import Http404
from mailing.forms import LetterForm
from mailing.models import Letter


class LetterCreateView(LoginRequiredMixin, CreateView):
    model = Letter
    form_class = LetterForm

    def get_success_url(self):
        return reverse('mailing:letter', args=[self.object.pk])

    def form_valid(self, form):
        new_post = form.save()
        new_post.author = self.request.user
        return super().form_valid(form)


class LetterDetailView(LoginRequiredMixin, DetailView):
    model = Letter

    def get_object(self, queryset=None):
        letter = super().get_object()
        if letter.owner == self.request.user or self.request.user.is_manager:
            return letter
        else:
            raise Http404


class LetterListView(LoginRequiredMixin, ListView):
    model = Letter

    def get_queryset(self):
        letter_list = super().get_queryset()
        if self.request.user.is_manager:
            return letter_list
        else:
            return letter_list.filter(owner=self.request.user)


class LetterUpdateView(LoginRequiredMixin, UpdateView):
    model = Letter
    form_class = LetterForm
    
    def get_object(self, queryset=None):
        letter = super().get_object()
        if letter.owner == self.request.user:
            return letter
        else:
            raise Http404

    def get_success_url(self):
        return reverse('mailing:letter', args=[self.object.pk])


class LetterDeleteView(DeleteView):
    model = Letter
    success_url = reverse_lazy("mailing:letter_list")


from django.shortcuts import render

# Create your views here.
