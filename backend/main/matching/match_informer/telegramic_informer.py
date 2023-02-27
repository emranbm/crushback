from asgiref.sync import sync_to_async

from main.matching.match_informer.base import MatchInformer
from main.models import MatchedRecord
from main.telegrambot.engine import TelegramBotEngine
from main.utils.async_utils import get_model_prop


class TelegramicInformer(MatchInformer):
    async def inform_match(self, matched_record: MatchedRecord) -> bool:
        app = TelegramBotEngine.get_app()
        user1 = await get_model_prop(matched_record, 'left_user')
        user2 = await get_model_prop(matched_record, 'right_user')
        await app.bot.send_message(user1.telegram_chat_id,
                                   f"Congratulations!\n"
                                   f"Your crush @{user2.telegram_username} already has a crush on you!\n"
                                   f"She/He is also informed! Now you both know that you have a crush on each other.\n"
                                   f"Have a good love!")
        await app.bot.send_message(user2.telegram_chat_id,
                                   f"Congratulations!\n"
                                   f"Your crush @{user1.telegram_username} already has a crush on you!\n"
                                   f"She/He is also informed! Now you both know that you have a crush on each other.\n"
                                   f"Have a good love!")
        return True
