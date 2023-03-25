import asyncio
from argparse import ArgumentParser
from datetime import datetime
from time import sleep

from django.core.management import BaseCommand

from main.matching.engine import MatchingEngine
from main.matching.match_finder.telegram_match_finder import TelegramMatchFinder
from main.matching.match_informer.telegramic_informer import TelegramicInformer


class Command(BaseCommand):
    help = 'Check if any new matches has occurred and saves them in database.'
    match_finder: TelegramMatchFinder

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument('--period', action='store',
                            help="Waiting period between checks. (seconds)",
                            type=int,
                            default=600)

    def handle(self, *args, **options):
        period_seconds = options['period']
        self.stdout.write(f"Starting to check matches every {period_seconds} seconds ...")
        self.match_finder = TelegramMatchFinder()
        while True:
            asyncio.run(self.find_new_matches())
            sleep(period_seconds)

    async def find_new_matches(self):
        self.stdout.write(f"({datetime.now()}) Finding new matches...")
        new_records = await self.match_finder.save_new_matched_records()
        self.stdout.write(f"({datetime.now()}) Done!")
        self.stdout.write(f"{len(new_records)} new matches have been detected and saved.")
