from telethon.tl.custom import Message

from base import TelegramBotTestCase


class PrivacyCommandTest(TelegramBotTestCase):
    async def test_should_reply_appropriate_message(self):
        async with self._create_conversation() as conv:
            await conv.send_message('/botmoncheck')
            msg: Message = await conv.get_response()
            self.assertEqual("Pong!", msg.text.strip())
