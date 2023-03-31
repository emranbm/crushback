from main import testing_utils
from main.telegrambot.command_handlers.botmoncheck_command_handler import BotmonCheckCommandHandler
from main.telegrambot.command_handlers.command_handler_with_metrics import CommandHandlerWithMetrics
from main.telegrambot.command_handlers.test_base_test_case import CommandHandlerBaseTestCase


class StartCommandHandlerTest(CommandHandlerBaseTestCase):
    # Override
    def get_handler(self) -> CommandHandlerWithMetrics:
        return BotmonCheckCommandHandler()

    async def test_should_not_contain_any_db_query(self):
        with self.assertNumQueries(0):
            await self.trigger_handler()
