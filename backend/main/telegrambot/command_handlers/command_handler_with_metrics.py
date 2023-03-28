from datetime import datetime
from typing import Optional, Callable, Awaitable

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from main import metrics


class CommandHandlerWithMetrics(CommandHandler):
    command: str

    def __init__(self, command: str, handler: Optional[Callable[[Update, ContextTypes.DEFAULT_TYPE], Awaitable[None]]] = None):
        super().__init__(command, self._handle_command)
        self.command = command
        self._passed_handler = handler

    async def _handle_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        start_time = datetime.now()
        await self.handle_command(update, context)
        delta = datetime.now() - start_time
        metrics.SERVER_LATENCY.labels(agent="telegrambot", action=self.command).observe(delta.seconds)

    async def handle_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self._passed_handler is None:
            raise NotImplementedError("Either implement this method or pass handler to the constructor.")
        else:
            self._passed_handler(update, context)
