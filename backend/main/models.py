from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(null=False, blank=True, default='', max_length=64)
    last_name = models.CharField(null=False, blank=True, default='', max_length=64)
    telegram_username = models.CharField(max_length=32)
    telegram_chat_id = models.BigIntegerField()
