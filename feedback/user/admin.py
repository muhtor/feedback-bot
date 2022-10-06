from django.contrib import admin
from .models import TelegramUser, ClientUser
# Register your models here.

admin.site.register(TelegramUser)
admin.site.register(ClientUser)
