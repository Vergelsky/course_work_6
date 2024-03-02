from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse

from mailing.forms import LetterForm
from mailing.models import Letter


class LetterCreateView(CreateView):
    model = Letter
    form_class = LetterForm

    def get_success_url(self):
        return reverse('mailing:letter', args=[self.object.pk])

    def form_valid(self, form):
        new_post = form.save()
        new_post.author = self.request.user
        return super().form_valid(form)


class LetterDetailView(DetailView):
    model = Letter


class LetterListView(ListView):
    model = Letter


class LetterUpdateView(UpdateView):
    model = Letter
    form_class = LetterForm

    def get_success_url(self):
        return reverse('mailing:letter', args=[self.object.pk])


class LetterDeleteView(DeleteView):
    model = Letter
    success_url = reverse_lazy("mailing:letter_list")


from django.shortcuts import render

# Create your views here.
