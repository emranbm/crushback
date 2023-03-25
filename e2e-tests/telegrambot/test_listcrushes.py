from telethon.tl.custom import Message, Conversation

import testing_utils
from base import TelegramBotTestCase


class ListCrushesCommandTest(TelegramBotTestCase):
    async def test_should_show_user_crushes(self):
        async with self._create_conversation() as conv:
            await testing_utils.add_crush("my_crush1", conv)
            await testing_utils.add_crush("my_crush2", conv)
            await conv.send_message("/listcrushes")
            msg: Message = await conv.get_response()
            self.assertEqual("@my_crush1\n@my_crush2", msg.text)

    async def test_should_promote_addcrush_if_no_crushes_exist(self):
        async with self._create_conversation() as conv:
            await conv.send_message("/listcrushes")
            msg: Message = await conv.get_response()
            self.assertTrue("/addcrush" in msg.text)
