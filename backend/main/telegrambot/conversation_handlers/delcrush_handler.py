from datetime import datetime
from enum import Enum

import telegram
from asgiref.sync import sync_to_async
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, ContextTypes, MessageHandler, filters

from main import metrics
from main.models import Crush
from main.telegrambot import utils
from main.telegrambot.command_handlers.command_handler_with_metrics import CommandHandlerWithMetrics


class _State(Enum):
    START = 0
    RECEIVE_USERNAME = 1


class DelcrushHandler(ConversationHandler):
    def __init__(self):
        super().__init__(
            entry_points=[CommandHandler('delcrush', self._on_delcruch)],
            states={
                _State.RECEIVE_USERNAME: [
                    MessageHandler(filters.Regex("^@.*"), self._on_crush_username_entered),
                    MessageHandler(filters.ALL & (~filters.COMMAND), self._on_wrong_username_format),
                ]
            },
            fallbacks=[CommandHandlerWithMetrics("cancel", self._on_cancel)], )

    @staticmethod
    async def _on_delcruch(update: Update, context: ContextTypes.DEFAULT_TYPE) -> _State:
        await update.message.reply_text("Send the username to delete from crushes.\n"
                                        "Or /cancel.")
        return _State.RECEIVE_USERNAME

    @staticmethod
    async def _on_wrong_username_format(update: Update, context: ContextTypes.DEFAULT_TYPE) -> _State:
        await update.message.reply_text("Please send the username in the form of @username\n"
                                        "Or /cancel")
        return _State.RECEIVE_USERNAME

    @staticmethod
    async def _on_crush_username_entered(update: Update, context: ContextTypes.DEFAULT_TYPE) -> _State:
        start_time = datetime.now()
        user = await utils.create_or_update_user(update)
        crush_username = update.message.text
        try:
            crush = await Crush.objects.aget(crusher=user, telegram_username=crush_username.lstrip("@"))
            await sync_to_async(crush.delete)()
        except Crush.DoesNotExist:
            await update.message.reply_text("Username not found in the crushes list. Please check and try again.")
        except Exception:
            message = render_to_string('unexpected_error.html')
            await update.message.reply_html(message)
        else:
            message = render_to_string('crush_deleted_ack.html', {'crush_username': crush_username})
            await update.message.reply_html(message)
        elapsed_time = datetime.now() - start_time
        metrics.SERVER_LATENCY.labels(agent="telegrambot", action="delcrush").observe(elapsed_time.seconds)
        return ConversationHandler.END

    @staticmethod
    async def _on_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> _State:
        await update.message.reply_text("Canceled!")
        return ConversationHandler.END
