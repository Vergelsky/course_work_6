from mailinger.settings import EMAIL_HOST_USER
from users.models import User
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse


def send_new_password_email(email):
    user = User.objects.get(email=email)
    new_password = User.objects.make_random_password(length=12)
    send_mail(
        subject='Новый пароль от рассыльщика',
        message=f'Вот он: {new_password}',
        from_email=EMAIL_HOST_USER,
        recipient_list=[user.email]
    )
    user.set_password(new_password)
    user.save()
