from django.contrib.auth.models import AbstractUser
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    price = models.PositiveIntegerField()
    isBuyRequest = models.BooleanField(default=False)


class User(AbstractUser):
    phone_number = models.CharField(max_length=len("+989120001122"))
    first_name = models.CharField(null=False, blank=True, default='', max_length=64)
    last_name = models.CharField(null=False, blank=True, default='', max_length=64)
