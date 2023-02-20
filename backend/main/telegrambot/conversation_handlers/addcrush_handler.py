from enum import Enum

from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, ContextTypes, MessageHandler, filters


class _State(Enum):
    START = 0
    RECEIVE_USERNAME = 1


class AddCrushHandler(ConversationHandler):
    def __init__(self):
        super().__init__(
            entry_points=[CommandHandler('addcrush', self._on_addcruch)],
            states={
                _State.RECEIVE_USERNAME: [
                    MessageHandler(filters.Regex("^@.*"), self._crush_username_entered),
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
    async def _crush_username_entered(update: Update, context: ContextTypes.DEFAULT_TYPE) -> _State:
        await update.message.reply_text(f"OK! your crush is {update.message.text}!\n"
                                        "But I'm still under construction and can't save it.\n"
                                        "I swear nothing is even saved by me!\n\n"
                                        "Please text me later to check if I've got ready for you.")
        return ConversationHandler.END

    @staticmethod
    async def _on_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> _State:
        await update.message.reply_text("Canceled!")
        return ConversationHandler.END
