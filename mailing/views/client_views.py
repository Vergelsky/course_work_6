from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse

from django.http import Http404
from mailing.forms import ClientForm
from mailing.models import Client, Mailing

from django.contrib.auth.mixins import LoginRequiredMixin


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm

    def form_valid(self, form):
        client = form.save()
        client.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('mailing:client', args=[self.object.pk])


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client

    def get_object(self, queryset=None):
        client = super().get_object()
        if client.owner == self.request.user or self.request.user.is_manager:
            return client
        else:
            raise Http404


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_queryset(self):
        clients_list = super().get_queryset()
        if self.request.user.is_manager:
            return clients_list
        else:
            return clients_list.filter(owner=self.request.user)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm

    def get_object(self, queryset=None):
        client = super().get_object()
        if client.owner == self.request.user:
            return client
        else:
            raise Http404

    def get_success_url(self):
        return reverse('mailing:client', args=[self.object.pk])


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy("mailing:client_list")
