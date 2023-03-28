from django.template.loader import render_to_string
from telegram import Update
from telegram.ext import ContextTypes

from main.telegrambot import utils
from main.telegrambot.command_handlers.command_handler_with_metrics import CommandHandlerWithMetrics


class PrivacyCommandHandler(CommandHandlerWithMetrics):
    def __init__(self):
        super().__init__('privacy')

    # Override
    async def handle_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await utils.create_or_update_user(update)
        message = render_to_string('privacy_details.html')
        await update.message.reply_html(message)
