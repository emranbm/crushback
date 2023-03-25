from telethon.tl.custom import Message

import testing_utils
from base import TelegramBotTestCase


class DelCrushTest(TelegramBotTestCase):
    async def test_crush_gets_removed_from_list_when_deleted(self):
        async with self._create_conversation() as conv:
            await testing_utils.add_crush("crush1", conv)
            await testing_utils.add_crush("crush2", conv)
            await conv.send_message("/delcrush")
            await conv.get_response()
            await conv.send_message("@crush1")
            await conv.get_response()
            await conv.send_message("/listcrushes")
            msg: Message = await conv.get_response()
            self.assertFalse("crush1" in msg.text)
