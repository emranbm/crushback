import asyncio

from telethon.tl.custom import Message

import testing_utils
from base import TelegramBotTestCase


class AddCrushTest(TelegramBotTestCase):
    async def test_user_should_be_informed_if_his_crush_is_matched(self):
        async with self._create_conversation(1) as conv:
            await conv.send_message('/addcrush')
            await conv.get_response()
            await conv.send_message(f'@{self.clients[1]["username"]}')
            await conv.get_response()
        async with self._create_conversation(2) as conv:
            await conv.send_message('/addcrush')
            await conv.get_response()
            await conv.send_message(f'@{self.clients[0]["username"]}')
            await conv.get_response()  # Crush saved ack
            msg: Message = await conv.get_response(timeout=testing_utils.CHECK_MATCH_PERIOD_SECONDS + 2)  # Crush matched message
            self.assertTrue("congratulations" in msg.text.lower())

    async def test_cancel_should_work(self):
        async with self._create_conversation() as conv:
            await conv.send_message('/addcrush')
            await conv.get_response()
            await conv.send_message('/cancel')
            msg: Message = await conv.get_response()
            self.assertTrue("canceled" in msg.text.lower())

    @testing_utils.is_slow
    async def test_user_should_be_informed_only_after_the_configured_delay(self):
        await testing_utils.restart_services(additional_env={
            'CRUSHBACK_NEW_CRUSH_MATCH_FREEZE_MINUTES': '1'
        })
        async with self._create_conversation(1) as conv:
            await conv.send_message('/addcrush')
            await conv.get_response()
            await conv.send_message(f'@{self.clients[1]["username"]}')
            await conv.get_response()
        async with self._create_conversation(2) as conv:
            await conv.send_message('/addcrush')
            await conv.get_response()
            await conv.send_message(f'@{self.clients[0]["username"]}')
            await conv.get_response()  # Crush saved ack
            with self.assertRaises(asyncio.exceptions.TimeoutError):
                await conv.get_response(timeout=testing_utils.CHECK_MATCH_PERIOD_SECONDS + 3)
            msg: Message = await conv.get_response(timeout=testing_utils.CHECK_MATCH_PERIOD_SECONDS + 63)  # Crush matched message
            self.assertTrue("congratulations" in msg.text.lower())
