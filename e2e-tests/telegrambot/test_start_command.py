from telethon.tl.custom import Message

from base import TelegramBotTestCase


class StartCommandTest(TelegramBotTestCase):
    async def test_should_reply_appropriate_message(self):
        async with self._create_conversation() as conv:
            await conv.send_message('/start')
            msg: Message = await conv.get_response()
            self.assertTrue("crush" in msg.text.lower())
