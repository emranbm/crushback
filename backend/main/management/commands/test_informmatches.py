from unittest.mock import MagicMock, AsyncMock

from django.test import TestCase

from main import testing_utils
from main.management.commands.informmatches import Command
from main.matching.match_finder.telegram_match_finder import TelegramMatchFinder


class InformMatchesTest(TestCase):
    async def test_should_not_inform_already_informed_matches(self):
        await testing_utils.create_user_and_their_crush_async("tg1", "tg2")
        await testing_utils.create_user_and_their_crush_async("tg2", "tg1")
        await TelegramMatchFinder().save_new_matched_records()
        command_handler = Command()
        command_handler.match_informer = AsyncMock()
        await command_handler.inform_matches()
        await command_handler.inform_matches()
        command_handler.match_informer.inform_match.assert_called_once()
