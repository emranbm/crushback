import telegram.constants
from django.template.loader import render_to_string
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

from main.telegrambot import utils
from main.telegrambot.conversation_handlers.addcrush_handler import AddcrushHandler


class TelegramBot:
    @staticmethod
    def run(token: str, proxy_url: str = None) -> None:
        app_builder = ApplicationBuilder().token(token)
        if proxy_url is not None:
            app_builder = app_builder \
                .proxy_url(proxy_url) \
                .get_updates_proxy_url(proxy_url)
        app = app_builder.build()
        app.add_handler(CommandHandler('start', TelegramBot._on_start))
        app.add_handler(AddcrushHandler())
        app.run_polling()

    @staticmethod
    async def _on_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await utils.create_or_update_user(update)
        message = render_to_string('start_command_reply.html', {'update': update})
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=message,
                                       parse_mode=telegram.constants.ParseMode.HTML)
