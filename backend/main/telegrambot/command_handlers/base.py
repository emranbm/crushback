from abc import abstractmethod, ABC
from datetime import datetime

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from main import metrics


class CommandHandlerBase(CommandHandler, ABC):
    command: str

    def __init__(self, command: str):
        super().__init__(command, self._handle_command)
        self.command = command

    async def _handle_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        start_time = datetime.now()
        await self.handle_command(update, context)
        delta = datetime.now() - start_time
        metrics.SERVER_LATENCY.labels(agent="telegrambot", action=self.command).observe(delta.seconds)

    @abstractmethod
    async def handle_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        pass
