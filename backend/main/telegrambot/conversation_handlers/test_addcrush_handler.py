from django.test import TestCase

from main import testing_utils
from main.models import Crush
from main.telegrambot.conversation_handlers.addcrush_handler import AddcrushHandler


class AddcrushHandlerTest(TestCase):
    def setUp(self) -> None:
        self.user = testing_utils.create_test_user()

    async def test_crush_should_save(self):
        update = testing_utils.create_default_update()
        context = testing_utils.create_default_context()
        update.message.text = "@crush_user"
        await AddcrushHandler()._on_crush_username_entered(update, context)
        self.assertTrue(await Crush.objects.filter(crusher=self.user, telegram_username="crush_user").aexists(),
                        "Crush not found in database.")
