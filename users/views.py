from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


# Create your views here.
class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register_form.html'


def confirm_email(request, token):
    user = User.objects.filter(verification_code=token)
    if user.exists():
        user = User.objects.get(verification_code=token)
        user.is_active = True
        user.verification_code = ''
        user.save()
        return render(request, 'users/confirm_email.html', {'title': 'Почта подтверждена'})
    else:
        return render(request, 'users/confirm_email.html', {'title': 'Неверный код подтверждения'})


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    template_name = 'users/profile_form.html'

    def get_object(self, queryset=None):
        return self.request.user


class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy("users:login")
