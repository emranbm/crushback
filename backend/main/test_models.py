from django.core.exceptions import ValidationError
from django.test import TestCase

from main.models import Crush, User


class CrushTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user("test")

    def test_cant_save_crush_without_contact_point(self):
        with self.assertRaises(ValidationError):
            Crush(name="test", crusher=self.user).save()

    def test_can_save_crush_without_name(self):
        Crush(telegram_username="test", crusher=self.user).save()
