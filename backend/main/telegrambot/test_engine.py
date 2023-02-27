from asgiref.sync import sync_to_async
from django.test import TestCase

from main import models, testing_utils
from main.telegrambot.engine import TelegramBotEngine


# noinspection PyMethodMayBeStatic
class StartCommandTest(TestCase):
    async def test_should_reply(self):
        update = testing_utils.create_default_update()
        context = testing_utils.create_default_context()
        await TelegramBotEngine._on_start(update, context)
        send_message_kwargs = context.bot.send_message.call_args.kwargs
        self.assertTrue(f"Hi {testing_utils.TEST_USER_FIRST_NAME}" in send_message_kwargs['text'],
                        f"Unexpected reply message: {send_message_kwargs['text']}")

    async def test_should_save_new_user(self):
        users_count = await models.User.objects.acount()
        update = testing_utils.create_default_update()
        context = testing_utils.create_default_context()
        await TelegramBotEngine._on_start(update, context)
        self.assertEqual(users_count + 1, await models.User.objects.acount())
        user = await models.User.objects.aget(telegram_user_id=testing_utils.TEST_USER_ID)
        self.assertEqual(testing_utils.TEST_USER_ID, user.telegram_user_id)
        self.assertEqual(testing_utils.TEST_CHAT_ID, user.telegram_chat_id)
        self.assertEqual(testing_utils.TEST_USER_FIRST_NAME, user.first_name)
        self.assertEqual(testing_utils.TEST_USER_LAST_NAME, user.last_name)

    async def test_should_not_update_general_info_of_existing_user(self):
        await testing_utils.create_test_user_async()
        update = testing_utils.create_default_update()
        context = testing_utils.create_default_context()
        await TelegramBotEngine._on_start(update, context)
        user = await models.User.objects.aget(telegram_user_id=testing_utils.TEST_USER_ID)
        self.assertEqual(testing_utils.TEST_USER_FIRST_NAME + " (custom)", user.first_name)
        self.assertEqual(testing_utils.TEST_USER_LAST_NAME + " (custom)", user.last_name)

    async def test_should_update_username_if_changed(self):
        update = testing_utils.create_default_update()
        context = testing_utils.create_default_context()
        await TelegramBotEngine._on_start(update, context)
        new_username = testing_utils.TEST_USER_USERNAME + "_new"
        update.effective_user.username = new_username
        await TelegramBotEngine._on_start(update, context)
        user = await models.User.objects.aget(telegram_user_id=testing_utils.TEST_USER_ID)
        self.assertEqual(new_username, user.telegram_username)

    async def test_should_update_chat_id_if_changed(self):
        update = testing_utils.create_default_update()
        context = testing_utils.create_default_context()
        await TelegramBotEngine._on_start(update, context)
        new_chat_id = testing_utils.TEST_CHAT_ID + 1
        update.effective_chat.id = new_chat_id
        await TelegramBotEngine._on_start(update, context)
        user = await models.User.objects.aget(telegram_user_id=testing_utils.TEST_USER_ID)
        self.assertEqual(new_chat_id, user.telegram_chat_id)
