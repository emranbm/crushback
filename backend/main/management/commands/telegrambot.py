from django.core.management import BaseCommand

from main.telegrambot.bot import TelegramBot


class Command(BaseCommand):
    help = 'Manages Telegram bot agent'

    def add_arguments(self, parser):
        parser.add_argument('--token', action='store',
                            help="Telegram bot token.", required=True)
        parser.add_argument('--proxy', action='store',
                            help="Optional proxy URL to be used. e.g. socks5://127.0.0.1:9000")

    def handle(self, *args, **options):
        token = options['token']
        proxy_url = options.get('proxy')
        self.stdout.write("Running the bot...")
        TelegramBot.run(token, proxy_url)
