from unittest.mock import AsyncMock

from django.test import TestCase
from telegram.ext import Application

from main import testing_utils
from main.matching.match_informer.telegramic_informer import TelegramicInformer
from main.models import MatchedRecord


class TelegramicInformerTest(TestCase):
    @testing_utils.mock_telegram_bot_engine_async
    async def test_both_users_get_informed_when_matched(self, mocked_telegram_app: Application):
        user1 = await testing_utils.create_user_and_their_crush_async("tg1", "tg2")
        user2 = await testing_utils.create_user_and_their_crush_async("tg2", "tg1")
        record = MatchedRecord(left_user=user1, right_user=user2)
        informed = await TelegramicInformer().inform_match(record)
        self.assertTrue(informed)
        mocked_send_message: AsyncMock = mocked_telegram_app.bot.send_message
        self.assertEqual(2, mocked_send_message.call_count)
        self.assertEqual(user1.telegram_chat_id, mocked_send_message.call_args_list[0].kwargs['chat_id'])
        self.assertEqual(user2.telegram_chat_id, mocked_send_message.call_args_list[1].kwargs['chat_id'])
