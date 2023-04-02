from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings

from main.models import Crush, User, MatchedRecord


class CrushTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user("test")

    def test_cant_save_crush_without_contact_point(self):
        with self.assertRaises(Crush.NoContactPointError):
            Crush(name="test", crusher=self.user).save()

    def test_can_save_crush_without_name(self):
        Crush(telegram_username="test", crusher=self.user).save()

    def test_can_not_save_duplicate_crush(self):
        Crush(telegram_username="test", crusher=self.user).save()
        with self.assertRaises(ValidationError):
            Crush(telegram_username="test", crusher=self.user).save()
        self.assertEqual(1, Crush.objects.filter(telegram_username="test").count())

    @override_settings(MAX_CRUSHES=1)
    def test_can_not_save_more_than_limit(self):
        Crush(telegram_username="crush1", crusher=self.user).save()
        with self.assertRaises(Crush.MaxCrushesLimit):
            Crush(telegram_username="crush2", crusher=self.user).save()

    @override_settings(MAX_CRUSHES=0)
    def test_max_crush_of_0_is_assumed_as_no_limit(self):
        for i in range(0, 100):
            Crush(telegram_username=f"crush{i}", crusher=self.user).save()


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
