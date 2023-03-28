from django.template.loader import render_to_string
from telegram import Update
from telegram.ext import ContextTypes

from main.models import Crush
from main.telegrambot.command_handlers.command_handler_with_metrics import CommandHandlerWithMetrics


class ListCrushesHandler(CommandHandlerWithMetrics):
    def __init__(self):
        super().__init__('listcrushes')

    async def handle_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        crushes = [c async for c in Crush.objects.filter(crusher__telegram_user_id=update.effective_user.id).aiterator()]
        message = render_to_string('crushes_list.html', {'crushes': crushes})
        await update.message.reply_html(message)
