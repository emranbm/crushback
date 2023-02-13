from django.core.management import BaseCommand
from telegram import Update
from telegram.request._httpxrequest import HTTPXRequest
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# from _pysoxy import main as run_socks

HTTPXRequest()

class Command(BaseCommand):
    help = 'Manages Telegram bot agent'

    def add_arguments(self, parser):
        parser.add_argument('bot_token', type=str)
        parser.add_argument('--proxy', action='store',
                            help="Optional proxy URL to be used. e.g. socks5://127.0.0.1:9000")

    def handle(self, *args, **options):
        token = options['bot_token']
        app_builder = ApplicationBuilder().token(token)
        proxy = options.get('proxy', False)
        if proxy:
            app_builder = app_builder\
                .proxy_url(proxy)\
                .get_updates_proxy_url(proxy)
        app =  app_builder.build()
        app.add_handler(CommandHandler("start", Command.start))
        self.stdout.write("Starting telegrambot ...")
        app.run_polling()

    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(f'''
Hello {update.effective_user.first_name},
Thanks for texting me!
I'm newborn and still under construction...
Would you please text me later?
I'll love checking if your crush is already having a crushback on you!
        ''')
