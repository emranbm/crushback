from telethon.tl.custom import Message

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
            msg: Message = await conv.get_response(timeout=self.CHECK_MATCH_PERIOD_SECONDS + 1)  # Crush matched message
            self.assertTrue("congratulations" in msg.text.lower())
