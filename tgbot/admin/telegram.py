from django.contrib import admin

from tgbot.models.telegram import *


@admin.register(User)
class UserDefaultAdmin(admin.ModelAdmin):
    list_display = ('cid', 'username', 'name', 'lastname')
    ordering = ['cid', ]


@admin.register(UserAction)
class UserActionAdmin(admin.ModelAdmin):
    list_display = ('cid', 'name', 'dop', 'date_operation')
    ordering = ['-date_operation', 'cid']


@admin.register(Markup)
class MarkupDefaultAdmin(admin.ModelAdmin):
    ordering = ['name']


@admin.register(Message)
class MessageDefaultAdmin(admin.ModelAdmin):
    ordering = ['name']



