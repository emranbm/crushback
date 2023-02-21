import unittest
from unittest.mock import Mock, AsyncMock

from asgiref.sync import sync_to_async, async_to_sync
from telegram import Update
from telegram.ext import ContextTypes

from main import models
from main.models import User

TEST_USER_ID = 123
TEST_CHAT_ID = 456
TEST_USER_USERNAME = 'test_username'
TEST_USER_FIRST_NAME = 'first name'
TEST_USER_LAST_NAME = 'last name'


def create_test_user():
    return models.User.objects.create_user("internal_username",
                                           telegram_user_id=TEST_USER_ID,
                                           telegram_username=TEST_USER_USERNAME,
                                           telegram_chat_id=TEST_CHAT_ID,
                                           first_name=TEST_USER_FIRST_NAME + " (custom)",
                                           last_name=TEST_USER_LAST_NAME + " (custom)")


async def create_test_user_async() -> User:
    return await sync_to_async(create_test_user)()


def create_default_update() -> Update:
    update: Update = Mock()
    update.effective_user.id = TEST_USER_ID
    update.effective_user.username = TEST_USER_USERNAME
    update.effective_user.first_name = TEST_USER_FIRST_NAME
    update.effective_user.last_name = TEST_USER_LAST_NAME
    update.effective_chat.id = TEST_CHAT_ID
    return update


def create_default_context() -> ContextTypes.DEFAULT_TYPE:
    context: ContextTypes.DEFAULT_TYPE = Mock()
    context.bot.send_message = AsyncMock()
    return context
