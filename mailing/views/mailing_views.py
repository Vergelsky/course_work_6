from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse
from django.core.management import execute_from_command_line

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.http import Http404
from mailing.forms import MailingForm
from mailing.models import Mailing
from users.models import User


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm

    def get_success_url(self):
        return reverse('mailing:mailing', args=[self.object.pk])

    def form_valid(self, form):

        new_post = form.save()
        new_post.author = self.request.user
        return super().form_valid(form)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    def get_object(self, queryset=None):
        mailing = super().get_object()
        if mailing.owner == self.request.user or self.request.user.is_manager:
            return mailing
        else:
            raise Http404


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing

    def post(self, request, *args, **kwargs):
        pk = request.POST.get('pk', None)
        mailing = Mailing.objects.get(pk=pk)
        if mailing.status == 'started':
            mailing.status = 'ended'
            mailing.save()
        else:
            mailing.status = 'started'
            mailing.save()
        return HttpResponseRedirect(reverse_lazy('mailing:mailing_list'))
    def get_queryset(self):
        clients_list = super().get_queryset()
        if self.request.user.is_manager:
            return clients_list
        else:
            return clients_list.filter(owner=self.request.user)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_update.html'

    def get_success_url(self):
        return reverse('mailing:mailing', args=[self.object.pk])

    def get_object(self, queryset=None):
        mailing = super().get_object()
        if mailing.owner == self.request.user:
            return mailing
        else:
            raise Http404


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy("mailing:mailing_list")

    def get_object(self, queryset=None):
        mailing = super().get_object()
        if mailing.owner == self.request.user:
            return mailing
        else:
            raise Http404


from django.shortcuts import render

# Create your views here.
