import random
import string

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django_prometheus.models import ExportModelOperationsMixin


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


class User(AbstractUser, Contactable, ExportModelOperationsMixin("User")):
    first_name = models.CharField(null=False, blank=True, default='', max_length=64)
    last_name = models.CharField(null=False, blank=True, default='', max_length=64)
    telegram_user_id = models.BigIntegerField(null=True, blank=True, unique=True)
    telegram_chat_id = models.BigIntegerField(null=True, blank=True)

    @staticmethod
    def generate_random_username() -> str:
        return ''.join(random.choice(string.ascii_letters) for i in range(64))


class Crush(Contactable, ExportModelOperationsMixin("Crush")):
    name = models.CharField(null=False, blank=True, default='', max_length=64)
    crusher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="crushes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            # Should be checked differently whenever contact points other than Telegram are also supported.
            models.UniqueConstraint(fields=['telegram_username', 'crusher'], name="duplicate_crush_preventer")
        ]

    class NoContactPointError(BusinessLogicError):
        def __init__(self):
            super().__init__("Crush should have at least one contact point.")

    class MaxCrushesLimit(BusinessLogicError):
        def __init__(self):
            super().__init__(f"Maximum number of crushes ({settings.MAX_CRUSHES}) has been reached!")

    def clean(self):
        super().clean()
        self._check_at_least_one_contact_point_should_be_non_null()
        self._check_max_crushes_limit()

    def _check_at_least_one_contact_point_should_be_non_null(self) -> None:
        if not self.telegram_username:
            raise Crush.NoContactPointError()

    def _check_max_crushes_limit(self) -> None:
        is_edit = self.pk is not None
        if is_edit:
            return
        if settings.MAX_CRUSHES == 0:
            return
        current_count = Crush.objects.filter(crusher_id=self.crusher_id).count()
        if current_count >= settings.MAX_CRUSHES:
            raise Crush.MaxCrushesLimit()


class MatchedRecord(_AutoCleanedModel, ExportModelOperationsMixin("MatchedRecord")):
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

    @staticmethod
    def create_new_match(user_id_1: int, user_id_2: int) -> "MatchedRecord":
        record = MatchedRecord(left_user_id=min(user_id_1, user_id_2),
                               right_user_id=max(user_id_1, user_id_2))
        record.save()
        return record
