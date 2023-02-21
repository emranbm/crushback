import unittest
from unittest import skip

from asgiref.sync import async_to_sync
from django.test import TestCase

from main.models import Crush
from main.telegrambot import test_utils
from main.telegrambot.conversation_handlers.addcrush_handler import AddcrushHandler


class AddcrushHandlerTest(TestCase):
    def setUp(self) -> None:
        test_utils.create_test_user()

    @skip("Feature not implemented yet")
    async def test_crush_should_save(self):
        update = test_utils.create_default_update()
        context = test_utils.create_default_context()
        update.message.text = "@crush_user"
        await AddcrushHandler()._on_crush_username_entered(update, context)
        self.assertEqual(1, await Crush.objects.acount())
