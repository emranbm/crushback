import random
import string

from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

from main import models


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
        app.run_polling()

    @staticmethod
    async def _on_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await TelegramBot._create_or_update_user(update)
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f'''
Hello {update.effective_user.first_name},
Thanks for texting me!
I'm newborn and still under construction...
Would you please text me later?
I'll love checking if your crush is already having a crushback on you!
        ''')

    @staticmethod
    async def _create_or_update_user(update: Update) -> models.User:
        (user, created) = await models.User.objects.aget_or_create(
            telegram_chat_id=update.effective_chat.id,
            defaults={
                'telegram_username': update.effective_user.username,
                'username': ''.join(random.choice(string.ascii_letters) for i in range(64)),
                'first_name': update.effective_user.first_name,
                'last_name': update.effective_user.last_name or '',
            })
        if not created and user.telegram_username != update.effective_user.username:
            user.telegram_username = update.effective_user.username
            await sync_to_async(user.save)()
        return user
