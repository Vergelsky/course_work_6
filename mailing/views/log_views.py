from django.views.generic import ListView

from mailing.models import Log, Mailing

from django.contrib.auth.mixins import LoginRequiredMixin

class LogListView(LoginRequiredMixin, ListView):
    model = Log
    def get_queryset(self):
        logs_list = super().get_queryset()
        if self.request.user.is_manager:
            return logs_list
        else:
            logs = Log.objects.filter(mailing=Mailing.objects.filter(owner=self.request.user).first())
            for mailing in Mailing.objects.filter(owner=self.request.user):
                logs.union(Log.objects.filter(mailing=mailing))
                print(logs)
            return logs
