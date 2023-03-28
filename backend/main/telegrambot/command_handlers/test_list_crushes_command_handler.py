from main import testing_utils
from main.telegrambot.command_handlers.command_handler_with_metrics import CommandHandlerWithMetrics
from main.telegrambot.command_handlers.list_crushes_handler import ListCrushesHandler
from main.telegrambot.command_handlers.test_base_test_case import CommandHandlerBaseTestCase


class ListCrushesCommandHandlerTest(CommandHandlerBaseTestCase):
    def get_handler(self) -> CommandHandlerWithMetrics:
        return ListCrushesHandler()

    async def test_should_promote_addcrush_command_when_no_crush_exists(self):
        resp = await self.trigger_handler()
        self.assertTrue("/addcrush" in resp)

    async def test_should_show_crush(self):
        user = await testing_utils.create_user_and_their_crush_async("me", "my_crush")
        update = testing_utils.create_default_update(user)
        resp = await self.trigger_handler(update)
        self.assertTrue("@my_crush" in resp)

    async def test_should_not_show_others_crushes(self):
        user1 = await testing_utils.create_user_and_their_crush_async("me", "my_crush")
        await testing_utils.create_user_and_their_crush_async("someone_else", "his_crush")
        update = testing_utils.create_default_update(user1)
        resp = await self.trigger_handler(update)
        self.assertTrue("@my_crush" in resp)
        self.assertFalse("@his_crush" in resp)
