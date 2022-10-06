from django.db import models
from django.db.models.signals import post_save


class ClientUser(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)

    class Meta:
        db_table = "client_user"
        verbose_name_plural = "Client Users"

    def __str__(self):
        return f"ID: {self.first_name} {self.last_name}"


class TelegramUser(models.Model):
    chat_id = models.IntegerField(default=0)
    username = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    timer = models.CharField(max_length=255, blank=True, null=True)
    text = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True)
    lang = models.CharField(max_length=10)
    step = models.SmallIntegerField(default=0)

    class Meta:
        db_table = "tg_user"
        verbose_name_plural = "Telegram Users"

    def __str__(self):
        return f"ID: {self.id} - {self.chat_id}"

