from django.contrib import admin

from mailing.models import Client, Letter, Log, Mailing


# Register your models here.
@admin.register(Client)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'owner')


@admin.register(Letter)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('title', 'name', 'owner')


@admin.register(Log)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('last_try_dt', 'last_try_dt', 'mailing')


@admin.register(Mailing)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'period')