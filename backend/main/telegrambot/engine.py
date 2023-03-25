import telegram.constants
from django.conf import settings
from django.template.loader import render_to_string
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, Application

from main.telegrambot import utils
from main.telegrambot.conversation_handlers.addcrush_handler import AddcrushHandler


class TelegramBotEngine:
    @staticmethod
    def get_app() -> Application:
        app_builder = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN)
        proxy_url = settings.TELEGRAM_PROXY_URL
        if proxy_url is not None:
            app_builder = app_builder \
                .proxy_url(proxy_url) \
                .get_updates_proxy_url(proxy_url)
        return app_builder.build()

    @staticmethod
    def run() -> None:
        app = TelegramBotEngine.get_app()
        app.add_handler(CommandHandler('start', TelegramBotEngine._on_start))
        app.add_handler(AddcrushHandler())
        app.run_polling(drop_pending_updates=True)

    @staticmethod
    async def _on_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await utils.create_or_update_user(update)
        message = render_to_string('start_command_reply.html', {'update': update})
        await update.message.reply_html(message)
