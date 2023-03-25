from enum import Enum

import telegram
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, ContextTypes, MessageHandler, filters

from main.models import Crush
from main.telegrambot import utils


class _State(Enum):
    START = 0
    RECEIVE_USERNAME = 1


class AddcrushHandler(ConversationHandler):
    def __init__(self):
        super().__init__(
            entry_points=[CommandHandler('addcrush', self._on_addcruch)],
            states={
                _State.RECEIVE_USERNAME: [
                    MessageHandler(filters.Regex("^@.*"), self._on_crush_username_entered),
                    MessageHandler(filters.ALL & (~filters.COMMAND), self._on_wrong_username_format),
                ]
            },
            fallbacks=[CommandHandler("cancel", self._on_cancel)], )

    @staticmethod
    async def _on_addcruch(update: Update, context: ContextTypes.DEFAULT_TYPE) -> _State:
        await update.message.reply_text("OK! Please send me your crush's username.\n"
                                        "Or /cancel.")
        return _State.RECEIVE_USERNAME

    @staticmethod
    async def _on_wrong_username_format(update: Update, context: ContextTypes.DEFAULT_TYPE) -> _State:
        await update.message.reply_text("Please send the username in the form of @username\n"
                                        "Or /cancel")
        return _State.RECEIVE_USERNAME

    @staticmethod
    async def _on_crush_username_entered(update: Update, context: ContextTypes.DEFAULT_TYPE) -> _State:
        user = await utils.create_or_update_user(update)
        crush_username = update.message.text
        try:
            await Crush.objects.acreate(crusher=user, telegram_username=crush_username.lstrip("@"))
        except ValidationError:
            message = render_to_string('duplicate_add_crush_error.html')
            await update.message.reply_html(message)
        except Exception:
            message = render_to_string('unexpected_error.html')
            await update.message.reply_html(message)
        else:
            message = render_to_string('crush_saved_ack.html', {'crush_username': crush_username})
            await update.message.reply_html(message)
        return ConversationHandler.END

    @staticmethod
    async def _on_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> _State:
        await update.message.reply_text("Canceled!")
        return ConversationHandler.END
