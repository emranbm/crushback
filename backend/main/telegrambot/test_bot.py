from unittest.mock import Mock, AsyncMock

from django.test import TestCase
from telegram import Update
from telegram.ext import ContextTypes

from main.telegrambot.bot import TelegramBot


# noinspection PyMethodMayBeStatic
class TelegramBotTest(TestCase):
    async def test_start_command_should_reply(self):
        update: Update = Mock()
        update.effective_user.username = 'test'
        update.effective_user.first_name = 'first name'
        update.effective_user.last_name = 'last name'
        update.effective_chat.id = 123

        context: ContextTypes.DEFAULT_TYPE = Mock()
        context.bot.send_message = AsyncMock()
        await TelegramBot._on_start(update, context)
        context.bot.send_message.assert_called()
