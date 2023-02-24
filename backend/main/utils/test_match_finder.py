from django.test import TestCase

from main.models import User, Crush
from main.utils.match_finder import MatchFinder


class MatchFinderTest(TestCase):
    def test_nothing_is_found_with_empty_database(self):
        new_matches = MatchFinder.save_new_matched_records()
        self.assertEqual(0, len(new_matches))

    def test_users_get_matched_when_adding_each_other_telegram_usernames(self):
        user1 = User.objects.create_user("test1", telegram_username="tg1")
        user2 = User.objects.create_user("test2", telegram_username="tg2")
        Crush(telegram_username="tg2", crusher=user1).save()
        Crush(telegram_username="tg1", crusher=user2).save()
        new_matches = MatchFinder.save_new_matched_records()
        self.assertEqual(1, len(new_matches))
