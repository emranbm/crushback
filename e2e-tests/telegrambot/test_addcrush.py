from unittest import skip

from telethon.tl.custom import Message

from base import TelegramBotTestCase


class AddCrushTest(TelegramBotTestCase):
    async def test_should_reply_appropriate_message_on_addcrush_command(self):
        async with self._create_conversation() as conv:
            await conv.send_message('/addcrush')
            msg: Message = await conv.get_response()
            self.assertEqual("OK! Please send me your crush's username.\n"
                             "Or /cancel.(This is experimental and doesn't work yet!)",
                             msg.text)
            await conv.send_message('/cancel')

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
