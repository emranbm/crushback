from unittest.mock import Mock, AsyncMock

from asgiref.sync import sync_to_async
from django.test import TestCase
from telegram import Update
from telegram.ext import ContextTypes

from main import models
from main.telegrambot.bot import TelegramBot


# noinspection PyMethodMayBeStatic
class StartCommandTest(TestCase):
    TEST_USER_ID = 123
    TEST_CHAT_ID = 456
    TEST_USER_USERNAME = 'test_username'
    TEST_USER_FIRST_NAME = 'first name'
    TEST_USER_LAST_NAME = 'last name'

    def _create_default_update(self) -> Update:
        update: Update = Mock()
        update.effective_user.id = self.TEST_USER_ID
        update.effective_user.username = self.TEST_USER_USERNAME
        update.effective_user.first_name = self.TEST_USER_FIRST_NAME
        update.effective_user.last_name = self.TEST_USER_LAST_NAME
        update.effective_chat.id = self.TEST_CHAT_ID
        return update

    def _create_default_context(self) -> ContextTypes.DEFAULT_TYPE:
        context: ContextTypes.DEFAULT_TYPE = Mock()
        context.bot.send_message = AsyncMock()
        return context

    async def test_should_reply(self):
        update = self._create_default_update()
        context = self._create_default_context()
        await TelegramBot._on_start(update, context)
        send_message_kwargs = context.bot.send_message.call_args.kwargs
        self.assertTrue(f"Hi {self.TEST_USER_FIRST_NAME}" in send_message_kwargs['text'],
                        f"Unexpected reply message: {send_message_kwargs['text']}")

    async def test_should_save_new_user(self):
        users_count = await models.User.objects.acount()
        update = self._create_default_update()
        context = self._create_default_context()
        await TelegramBot._on_start(update, context)
        self.assertEqual(users_count + 1, await models.User.objects.acount())
        user = await models.User.objects.aget(telegram_user_id=self.TEST_USER_ID)
        self.assertEqual(self.TEST_USER_ID, user.telegram_user_id)
        self.assertEqual(self.TEST_CHAT_ID, user.telegram_chat_id)
        self.assertEqual(self.TEST_USER_FIRST_NAME, user.first_name)
        self.assertEqual(self.TEST_USER_LAST_NAME, user.last_name)

    async def test_should_not_update_general_info_of_existing_user(self):
        def create_user():
            models.User.objects.create_user("internal_username",
                                            telegram_user_id=self.TEST_USER_ID,
                                            telegram_username=self.TEST_USER_USERNAME,
                                            telegram_chat_id=self.TEST_CHAT_ID,
                                            first_name=self.TEST_USER_FIRST_NAME + " (custom)",
                                            last_name=self.TEST_USER_LAST_NAME + " (custom)")

        await sync_to_async(create_user)()
        update = self._create_default_update()
        context = self._create_default_context()
        await TelegramBot._on_start(update, context)
        user = await models.User.objects.aget(telegram_user_id=self.TEST_USER_ID)
        self.assertEqual(self.TEST_USER_FIRST_NAME + " (custom)", user.first_name)
        self.assertEqual(self.TEST_USER_LAST_NAME + " (custom)", user.last_name)

    async def test_should_update_username_if_changed(self):
        update = self._create_default_update()
        context = self._create_default_context()
        await TelegramBot._on_start(update, context)
        new_username = self.TEST_USER_USERNAME + "_new"
        update.effective_user.username = new_username
        await TelegramBot._on_start(update, context)
        user = await models.User.objects.aget(telegram_user_id=self.TEST_USER_ID)
        self.assertEqual(new_username, user.telegram_username)

    async def test_should_update_chat_id_if_changed(self):
        update = self._create_default_update()
        context = self._create_default_context()
        await TelegramBot._on_start(update, context)
        new_chat_id = self.TEST_CHAT_ID + 1
        update.effective_chat.id = new_chat_id
        await TelegramBot._on_start(update, context)
        user = await models.User.objects.aget(telegram_user_id=self.TEST_USER_ID)
        self.assertEqual(new_chat_id, user.telegram_chat_id)
