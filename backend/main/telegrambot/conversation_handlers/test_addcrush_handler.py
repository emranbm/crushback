from unittest.mock import patch

from django.test import TestCase, override_settings

from main import testing_utils
from main.business_error import BusinessLogicError
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
                        "Crush not found in database!")

    async def test_should_send_appropriate_message_on_duplicate_crush(self):
        await Crush.objects.acreate(crusher=self.user, telegram_username="crush_user")
        update = testing_utils.create_default_update()
        context = testing_utils.create_default_context()
        update.message.text = "@crush_user"
        await AddcrushHandler()._on_crush_username_entered(update, context)
        self.assertTrue("patient" in update.message.reply_html.call_args.args[0].lower())

    @override_settings(MAX_CRUSHES=3)
    async def test_should_hint_about_max_crushes_number_before_reaching_limit(self):
        update = testing_utils.create_default_update()
        context = testing_utils.create_default_context()
        update.message.text = "@crush_user"
        await AddcrushHandler()._on_crush_username_entered(update, context)
        testing_utils.assert_str_in("3", update.message.reply_html.call_args.args[0])

    @override_settings(MAX_CRUSHES=1)
    async def test_should_send_max_crushes_number_when_reached_limit(self):
        await Crush.objects.acreate(crusher=self.user, telegram_username="crush_user")
        update = testing_utils.create_default_update()
        context = testing_utils.create_default_context()
        update.message.text = "@crush_user_2"
        await AddcrushHandler()._on_crush_username_entered(update, context)
        testing_utils.assert_str_in("1", update.message.reply_text.call_args.args[0])

    async def test_should_reply_exact_message_of_business_logic_error_when_creating_crush(self):
        class SomeError(BusinessLogicError):
            def __init__(self):
                super().__init__("The exact message of error!")

        with patch.object(Crush.objects, 'acreate') as mocked_acreate:
            mocked_acreate.side_effect = SomeError()
            update = testing_utils.create_default_update()
            context = testing_utils.create_default_context()
            update.message.text = "@crush_user"
            await AddcrushHandler()._on_crush_username_entered(update, context)
            self.assertEqual("The exact message of error!", update.message.reply_text.call_args.args[0])
