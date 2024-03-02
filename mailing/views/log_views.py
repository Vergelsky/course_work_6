from django.views.generic import ListView

from mailing.models import Log


class LogListView(ListView):
    model = Log