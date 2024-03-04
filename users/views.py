from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView
from django.core.mail import send_mail

from blog.services import send_new_password_email
from mailinger.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import Http404


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


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    template_name = 'users/profile_form.html'

    def get_object(self, queryset=None):
        return self.request.user


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy("users:login")


class UserListView(LoginRequiredMixin, DeleteView):
    model = User

    def get_queryset(self):
        users_list = super().get_queryset()
        if self.request.user.is_manager:
            return users_list
        else:
            raise Http404


def user_list(request):
    context = {'objects_list': User.objects.all()}
    print(context)
    return render(request, 'users/user_list.html', context)

def toggle(request, pk):
    if request.method == 'POST':
        user = User.objects.get(pk=pk)
        user.is_active = not user.is_active
        user.save()
    return render(request, 'users/user_list.html', {'objects_list': User.objects.all()})


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            send_new_password_email(email)
            return redirect(reverse('users:login'))
        except Exception as ex:
            message = 'Такой почты не зарегистрировано', ex
            context = {
                'message': message
            }
            return render(request, 'users/forgot.html', context)
    else:
        return render(request, 'users/forgot.html')
