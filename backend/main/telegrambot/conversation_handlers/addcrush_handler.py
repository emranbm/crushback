from enum import Enum

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
                                        "Or /cancel."
                                        "(This is experimental and doesn't work yet!)")
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
        await Crush.objects.acreate(crusher=user, telegram_username=crush_username.lstrip("@"))
        await update.message.reply_text(f"OK! your crush ({crush_username}) has been saved.\n"
                                        "I won't tell anybody that you have a crush on someone.\n"
                                        "I will check periodically if she/he has also a crush on you; and if so, "
                                        "I'll send a private message to you both!\n"
                                        "Keep in touch with me!")
        return ConversationHandler.END

    @staticmethod
    async def _on_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> _State:
        await update.message.reply_text("Canceled!")
        return ConversationHandler.END
