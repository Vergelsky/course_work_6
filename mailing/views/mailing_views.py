from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse
from django.core.management import execute_from_command_line

from mailing.forms import MailingForm
from mailing.models import Mailing


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm

    def get_success_url(self):
        return reverse('mailing:mailing', args=[self.object.pk])

    def form_valid(self, form):

        new_post = form.save()
        new_post.author = self.request.user
        return super().form_valid(form)


class MailingDetailView(DetailView):
    model = Mailing


class MailingListView(ListView):
    model = Mailing


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_update.html'

    def get_success_url(self):
        return reverse('mailing:mailing', args=[self.object.pk])


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy("mailing:mailing_list")


from django.shortcuts import render

# Create your views here.
