from abc import abstractmethod, ABC

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes


class CommandHandlerBase(CommandHandler, ABC):
    def __init__(self, command: str):
        super().__init__(command, self.handle_command)

    @abstractmethod
    async def handle_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        pass
