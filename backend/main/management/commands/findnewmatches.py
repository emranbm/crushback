import asyncio
from datetime import datetime

from django.core.management import BaseCommand

from main.matching.match_finder.telegram_match_finder import TelegramMatchFinder


class Command(BaseCommand):
    help = 'Check if any new matches has occurred and save them in database.'
    match_finder: TelegramMatchFinder

    def handle(self, *args, **options):
        self.stdout.write(f"Starting to check matches ...")
        self.match_finder = TelegramMatchFinder()
        asyncio.run(self.find_new_matches())

    async def find_new_matches(self):
        self.stdout.write(f"({datetime.now()}) Finding new matches...")
        new_records = await self.match_finder.save_new_matched_records()
        self.stdout.write(f"({datetime.now()}) Done!")
        self.stdout.write(f"{len(new_records)} new matches have been detected and saved.")
