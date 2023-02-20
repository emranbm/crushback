import random
import string

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(null=False, blank=True, default='', max_length=64)
    last_name = models.CharField(null=False, blank=True, default='', max_length=64)
    telegram_user_id = models.BigIntegerField(null=True, unique=True)
    telegram_username = models.CharField(null=False, blank=True, default='', max_length=32)
    telegram_chat_id = models.BigIntegerField(null=True)

    @staticmethod
    def generate_random_username() -> str:
        return ''.join(random.choice(string.ascii_letters) for i in range(64))
