from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler


class TelegramBot:
    @staticmethod
    def run(token: str, proxy_url: str = None) -> None:
        app_builder = ApplicationBuilder().token(token)
        if proxy_url is not None:
            app_builder = app_builder \
                .proxy_url(proxy_url) \
                .get_updates_proxy_url(proxy_url)
        app = app_builder.build()
        app.add_handler(CommandHandler('start', _Commands.start))
        app.run_polling()


class _Commands:
    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f'''
Hello {update.effective_user.first_name},
Thanks for texting me!
I'm newborn and still under construction...
Would you please text me later?
I'll love checking if your crush is already having a crushback on you!
        ''')
