from random import randint

from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm
from django import forms
from django.core.mail import send_mail
from users.models import User


class UserRegisterForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2',)

    def save(self):
        user = super().save(commit=False)
        token = randint(100000000, 100000000000)
        user.verification_code = token
        user.is_active = False
        res = send_mail('Подтверждение адреса',
                        f"Для подтверждения адреса электронной почты, пожалуйста, перейдите по ссылке"
                        f"http://127.0.0.1:8000/users/confirm_email/{ token }",
                        'skyprothebest@mail.ru',
                        [user.email,])
        user.save()
        return user


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'about',)


