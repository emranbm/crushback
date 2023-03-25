from telethon.tl.custom import Message, Conversation

from base import TelegramBotTestCase


class ListCrushesCommandTest(TelegramBotTestCase):
    async def add_crush(self, username: str, conv: Conversation):
        await conv.send_message('/addcrush')
        await conv.get_response()
        await conv.send_message(f'@{username}')
        await conv.get_response()

    async def test_should_show_user_crushes(self):
        async with self._create_conversation() as conv:
            await self.add_crush("my_crush1", conv)
            await self.add_crush("my_crush2", conv)
            await conv.send_message("/listcrushes")
            msg: Message = await conv.get_response()
            self.assertEqual("@my_crush1\n@my_crush2", msg.text)

    async def test_should_promote_addcrush_if_no_crushes_exist(self):
        async with self._create_conversation() as conv:
            await conv.send_message("/listcrushes")
            msg: Message = await conv.get_response()
            self.assertTrue("/addcrush" in msg.text)
