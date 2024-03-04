from django.views.generic import ListView

from mailing.models import Log, Mailing

from django.contrib.auth.mixins import LoginRequiredMixin

class LogListView(LoginRequiredMixin, ListView):
    model = Log
    def get_queryset(self):
        #
        logs_list = super().get_queryset()
        if self.request.user.is_manager:
            return logs_list
        else:
            user_mailings = self.request.user.mailing_set.all()
            return logs_list.filter(mailing__in=user_mailings)
