from django.test import TestCase

from main import testing_utils
from main.matching.match_finder.telegram_match_finder import TelegramMatchFinder
from main.models import Crush, MatchedRecord
from main.telegrambot.conversation_handlers.addcrush_handler import AddcrushHandler
from main.telegrambot.conversation_handlers.delcrush_handler import DelcrushHandler


class AddcrushHandlerTest(TestCase):
    def setUp(self) -> None:
        self.user = testing_utils.create_test_user()

    async def test_crush_should_get_deleted(self):
        Crush.objects.acreate(crusher=self.user, telegram_username="crush_user")
        update = testing_utils.create_default_update()
        context = testing_utils.create_default_context()
        update.message.text = "@crush_user"
        await DelcrushHandler()._on_crush_username_entered(update, context)
        self.assertFalse(await Crush.objects.filter(crusher=self.user, telegram_username="crush_user").aexists(),
                         "The crush found in database!")

    async def test_should_not_delete_matched_record_when_crush_is_deleted(self):
        user = await testing_utils.create_user_and_their_crush_async("tg1", "tg2")
        await testing_utils.create_user_and_their_crush_async("tg2", "tg1")
        self.assertEqual(0, await MatchedRecord.objects.acount())
        await TelegramMatchFinder().save_new_matched_records()
        self.assertEqual(1, await MatchedRecord.objects.acount())

        update = testing_utils.create_default_update(user)
        context = testing_utils.create_default_context()
        update.message.text = "@tg2"
        await DelcrushHandler()._on_crush_username_entered(update, context)
        self.assertEqual(1, await MatchedRecord.objects.acount())
