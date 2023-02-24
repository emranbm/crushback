from django.core.exceptions import ValidationError
from django.test import TestCase

from main.models import Crush, User, MatchedRecord


class CrushTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user("test")

    def test_cant_save_crush_without_contact_point(self):
        with self.assertRaises(ValidationError):
            Crush(name="test", crusher=self.user).save()

    def test_can_save_crush_without_name(self):
        Crush(telegram_username="test", crusher=self.user).save()


class MatchedRecordTest(TestCase):
    def test_left_user_id_should_be_lower_than_right_user_id(self):
        user1 = User.objects.create_user("test1")
        user2 = User.objects.create_user("test2")
        wrong_record = MatchedRecord(left_user_id=max(user1.pk, user2.pk),
                                     right_user_id=min(user1.pk, user2.pk))
        with self.assertRaises(AssertionError):
            wrong_record.save()

    def test_multiple_records_with_same_users_should_be_forbidden(self):
        user1 = User.objects.create_user("test1")
        user2 = User.objects.create_user("test2")
        MatchedRecord.create_new_match(user1.pk, user2.pk)
        with self.assertRaises(ValidationError):
            MatchedRecord.create_new_match(user1.pk, user2.pk)
