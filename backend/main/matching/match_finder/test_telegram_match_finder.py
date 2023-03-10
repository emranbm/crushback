from django.test import TestCase

from main import testing_utils
from main.matching.match_finder.telegram_match_finder import TelegramMatchFinder


class TelegramMatchFinderTest(TestCase):
    async def test_nothing_is_found_with_empty_database(self):
        new_matches = await TelegramMatchFinder().save_new_matched_records()
        self.assertEqual(0, len(new_matches))

    async def test_users_get_matched_when_adding_each_others_telegram_usernames(self):
        await testing_utils.create_user_and_their_crush_async("tg1", "tg2")
        await testing_utils.create_user_and_their_crush_async("tg2", "tg1")
        new_matches = await TelegramMatchFinder().save_new_matched_records()
        self.assertEqual(1, len(new_matches))

    async def test_should_only_find_new_matches(self):
        await testing_utils.create_user_and_their_crush_async("tg1", "tg2")
        await testing_utils.create_user_and_their_crush_async("tg2", "tg1")
        new_matches = await TelegramMatchFinder().save_new_matched_records()
        self.assertEqual(1, len(new_matches))
        new_matches = await TelegramMatchFinder().save_new_matched_records()
        self.assertEqual(0, len(new_matches))

    async def test_should_not_match_with_different_crushes(self):
        await testing_utils.create_user_and_their_crush_async("tg1", "crush1")
        await testing_utils.create_user_and_their_crush_async("tg2", "crush2")
        new_matches = await TelegramMatchFinder().save_new_matched_records()
        self.assertEqual(0, len(new_matches))

    async def test_should_not_match_without_crushback(self):
        await testing_utils.create_user_and_their_crush_async("tg1", "crush1")
        await testing_utils.create_user_and_their_crush_async("crush1", "crush2")
        new_matches = await TelegramMatchFinder().save_new_matched_records()
        self.assertEqual(0, len(new_matches))
