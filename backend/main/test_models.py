from django.core.exceptions import ValidationError
from django.test import TestCase

from main.models import Crush


class CrushTest(TestCase):
    def test_cant_save_crush_without_contact_point(self):
        with self.assertRaises(ValidationError):
            Crush(name="test").save()

    def test_can_save_crush_without_name(self):
        Crush(telegram_username="test").save()
