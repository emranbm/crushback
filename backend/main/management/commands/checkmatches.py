import asyncio
from argparse import ArgumentParser
from datetime import datetime
from time import sleep

from django.core.management import BaseCommand

from main.matching.engine import MatchingEngine
from main.matching.match_finder.telegram_match_finder import TelegramMatchFinder
from main.matching.match_informer.telegramic_informer import TelegramicInformer


class Command(BaseCommand):
    help = 'Check if any new matches has occurred and send corresponding messages to the users.'
    matching_engine: MatchingEngine

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument('--period', action='store',
                            help="Waiting period between checks. (seconds)",
                            type=int,
                            default=600)

    def handle(self, *args, **options):
        period_seconds = options['period']
        self.stdout.write(f"Starting to check matches every {period_seconds} seconds ...")
        self.matching_engine = MatchingEngine(TelegramMatchFinder(), TelegramicInformer())
        while True:
            asyncio.run(self.check_match())
            sleep(period_seconds)

    async def check_match(self):
        self.stdout.write(f"({datetime.now()}) Finding and informing matches...")
        informed_matches = await self.matching_engine.inform_newly_matched_users()
        self.stdout.write(f"({datetime.now()}) Done!")
        self.stdout.write(f"{len(informed_matches)} new matches have been detected and informed.")
