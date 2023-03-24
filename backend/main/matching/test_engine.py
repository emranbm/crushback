from unittest.mock import Mock, AsyncMock

from asgiref.sync import sync_to_async
from django.test import TestCase
from telegram.ext import Application

from main import testing_utils
from main.matching.engine import MatchingEngine
from main.matching.match_finder.telegram_match_finder import TelegramMatchFinder
from main.matching.match_informer.telegramic_informer import TelegramicInformer
from main.models import MatchedRecord


class MatchingEngineTest(TestCase):
    async def test_informs_both_matched_users(self):
        user1 = await testing_utils.create_user_and_their_crush_async("tg1", "tg2")
        user2 = await testing_utils.create_user_and_their_crush_async("tg2", "tg1")
        matching_engine = MatchingEngine(TelegramMatchFinder(), AsyncMock())
        await matching_engine.inform_newly_matched_users()
        mocked_inform_match: Mock = matching_engine.match_informer.inform_match
        self.assertEqual(1, mocked_inform_match.call_count)
        matched_record: MatchedRecord = mocked_inform_match.call_args.args[0]
        self.assertEqual(user1.id, matched_record.left_user_id)
        self.assertEqual(user2.id, matched_record.right_user_id)

    @testing_utils.mock_telegram_bot_engine_async
    async def test_not_informs_irrelevant_users(self, mocked_telegram_app: Application):
        await testing_utils.create_user_and_their_crush_async("tg1", "tg2")
        await testing_utils.create_user_and_their_crush_async("tg2", "tg1")
        irrelevant_user = await testing_utils.create_user_and_their_crush_async("some_user", "some_crush")
        matching_engine = MatchingEngine(TelegramMatchFinder(), TelegramicInformer())
        await matching_engine.inform_newly_matched_users()
        self.assertEqual(2, mocked_telegram_app.bot.send_message.call_count)
        for call_args in mocked_telegram_app.bot.send_message.call_args_list:
            self.assertNotEqual(irrelevant_user.telegram_chat_id, call_args.kwargs['chat_id'])

    @testing_utils.mock_telegram_bot_engine_async
    async def test_informs_no_one_when_no_matching_happened(self, mocked_telegram_app: Application):
        await testing_utils.create_user_and_their_crush_async("tg1", "tg2")
        await testing_utils.create_user_and_their_crush_async("tg2", "tg3")
        matching_engine = MatchingEngine(TelegramMatchFinder(), TelegramicInformer())
        await matching_engine.inform_newly_matched_users()
        mocked_telegram_app.bot.send_message: Mock
        mocked_telegram_app.bot.send_message.assert_not_called()
