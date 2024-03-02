from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse

from mailing.forms import ClientForm
from mailing.models import Client


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('mailing:client', args=[self.object.pk])


class ClientDetailView(DetailView):
    model = Client

class ClientListView(ListView):
    model = Client


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('mailing:client', args=[self.object.pk])


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy("mailing:client_list")
