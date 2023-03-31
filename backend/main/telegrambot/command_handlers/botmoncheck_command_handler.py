from django.template.loader import render_to_string
from telegram import Update
from telegram.ext import ContextTypes

from main.telegrambot import utils
from main.telegrambot.command_handlers.command_handler_with_metrics import CommandHandlerWithMetrics


class BotmonCheckCommandHandler(CommandHandlerWithMetrics):
    def __init__(self):
        super().__init__('botmoncheck')

    # Override
    async def handle_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Pong!")
