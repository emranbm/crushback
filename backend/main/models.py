import random
import string

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class _AutoCleanedModel(models.Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_cleaned = False

    class Meta:
        abstract = True

    def clean(self):
        self.is_cleaned = True
        super().clean()

    def save(self, *args, **kwargs):
        if not self.is_cleaned:
            self.full_clean()
        super().save(*args, **kwargs)


class Contactable(_AutoCleanedModel):
    """
    Different ways of contacting someone is aggregated in this mixin.
    """
    telegram_username = models.CharField(null=False, blank=True, default='', max_length=32)

    class Meta:
        abstract = True


class User(AbstractUser, Contactable):
    first_name = models.CharField(null=False, blank=True, default='', max_length=64)
    last_name = models.CharField(null=False, blank=True, default='', max_length=64)
    telegram_user_id = models.BigIntegerField(null=True, blank=True, unique=True)
    telegram_chat_id = models.BigIntegerField(null=True, blank=True)

    @staticmethod
    def generate_random_username() -> str:
        return ''.join(random.choice(string.ascii_letters) for i in range(64))


class Crush(Contactable):
    name = models.CharField(null=False, blank=True, default='', max_length=64)
    crusher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="crushes")

    def clean(self):
        super().clean()
        self._check_at_least_one_contact_point_should_be_non_null()

    def _check_at_least_one_contact_point_should_be_non_null(self) -> None:
        if not self.telegram_username:
            raise ValidationError("Crush should have at least one contact point.")


class MatchedRecord(_AutoCleanedModel):
    # Convention: The user with lower id is left, and the one with greater id is right.
    left_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', null=False)
    right_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', null=False)
    matched_at = models.DateTimeField(auto_now_add=True)
    informed = models.BooleanField(null=False, default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['left_user', 'right_user'], name='unique_matched_record_users')
        ]

    def clean(self):
        if self.left_user_id >= self.right_user_id:
            raise AssertionError("Convention violated: The user with lower id should be left, and the one with greater id should be right.")
