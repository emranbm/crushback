from django.test import TestCase

from main.matching.match_finder.telegram_match_finder import TelegramMatchFinder
from main.models import User, Crush


class TelegramMatchFinderTest(TestCase):
    def test_nothing_is_found_with_empty_database(self):
        new_matches = TelegramMatchFinder().save_new_matched_records()
        self.assertEqual(0, len(new_matches))

    def _create_user_and_their_crush(self, self_telegram_username: str, crush_telegram_username: str) -> User:
        user = User.objects.create_user(f"{self_telegram_username}_local", telegram_username=self_telegram_username)
        Crush(telegram_username=crush_telegram_username, crusher=user).save()
        return user

    def test_users_get_matched_when_adding_each_others_telegram_usernames(self):
        self._create_user_and_their_crush("tg1", "tg2")
        self._create_user_and_their_crush("tg2", "tg1")
        new_matches = TelegramMatchFinder().save_new_matched_records()
        self.assertEqual(1, len(new_matches))

    def test_should_only_find_new_matches(self):
        self._create_user_and_their_crush("tg1", "tg2")
        self._create_user_and_their_crush("tg2", "tg1")
        new_matches = TelegramMatchFinder().save_new_matched_records()
        self.assertEqual(1, len(new_matches))
        new_matches = TelegramMatchFinder().save_new_matched_records()
        self.assertEqual(0, len(new_matches))

    def test_should_not_match_with_different_crushes(self):
        self._create_user_and_their_crush("tg1", "crush1")
        self._create_user_and_their_crush("tg2", "crush2")
        new_matches = TelegramMatchFinder().save_new_matched_records()
        self.assertEqual(0, len(new_matches))

    def test_should_not_match_without_crushback(self):
        self._create_user_and_their_crush("tg1", "crush1")
        self._create_user_and_their_crush("crush1", "crush2")
        new_matches = TelegramMatchFinder().save_new_matched_records()
        self.assertEqual(0, len(new_matches))
