from django.urls import path
from . import views
from utils.handlers import webhook

app_name = "pusher"

urlpatterns = [
    path('send/bot', webhook, name="webhook"),  # {{BASE_URL}}/feedback/send/bot
]