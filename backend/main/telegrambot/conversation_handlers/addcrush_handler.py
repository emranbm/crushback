from datetime import datetime
from enum import Enum

from django.conf import settings
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, ContextTypes, MessageHandler, filters

from main import metrics
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
            fallbacks=[MessageHandler(filters.COMMAND, self._on_cancel)], )

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
        start_time = datetime.now()
        user = await utils.create_or_update_user(update)
        crush_username = update.message.text
        try:
            await Crush.objects.acreate(crusher=user, telegram_username=crush_username.lstrip("@"))
        except Crush.MaxCrushesLimit as e:
            await update.message.reply_text(str(e))
        except ValidationError:
            message = render_to_string('duplicate_add_crush_error.html')
            await update.message.reply_html(message)
        except Exception:
            message = render_to_string('unexpected_error.html')
            await update.message.reply_html(message)
        else:
            message = render_to_string('crush_saved_ack.html', {
                'crush_username': crush_username,
                'max_crushes': settings.MAX_CRUSHES or 'infinite'})
            await update.message.reply_html(message)
        elapsed_time = datetime.now() - start_time
        metrics.SERVER_LATENCY.labels(agent="telegrambot", action="addcrush").observe(elapsed_time.seconds)
        return ConversationHandler.END

    @staticmethod
    async def _on_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> _State:
        await update.message.reply_text("'addcrush' operation canceled!")
        return ConversationHandler.END
