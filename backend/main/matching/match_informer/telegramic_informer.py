import telegram
from django.template.loader import render_to_string

from main.matching.match_informer.base import MatchInformer
from main.models import MatchedRecord
from main.telegrambot.engine import TelegramBotEngine
from main.utils.async_utils import get_model_prop


class TelegramicInformer(MatchInformer):
    async def inform_match(self, matched_record: MatchedRecord) -> bool:
        app = TelegramBotEngine.create_app()
        user1 = await get_model_prop(matched_record, 'left_user')
        user2 = await get_model_prop(matched_record, 'right_user')

        message_to_user1 = render_to_string('match_inform_message.html', {'user': user1, 'crush': user2})
        message_to_user2 = render_to_string('match_inform_message.html', {'user': user2, 'crush': user1})
        await app.bot.send_message(chat_id=user1.telegram_chat_id,
                                   text=message_to_user1,
                                   parse_mode=telegram.constants.ParseMode.HTML)
        await app.bot.send_message(chat_id=user2.telegram_chat_id,
                                   text=message_to_user2,
                                   parse_mode=telegram.constants.ParseMode.HTML)
        return True
