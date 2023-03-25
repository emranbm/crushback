import asyncio
from argparse import ArgumentParser
from datetime import datetime

from django.core.management import BaseCommand
from time import sleep

from main.matching.match_informer.telegramic_informer import TelegramicInformer
from main.models import MatchedRecord


class Command(BaseCommand):
    help = 'Informs new non-informed matches.'
    match_informer: TelegramicInformer

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument('--period', action='store',
                            help="Waiting period between checks. (seconds)",
                            type=int,
                            default=600)

    def handle(self, *args, **options):
        period_seconds = options['period']
        self.stdout.write(f"Starting to inform new matches every {period_seconds} seconds ...")
        self.match_informer = TelegramicInformer()
        while True:
            asyncio.run(self.inform_matches())
            sleep(period_seconds)

    async def inform_matches(self):
        self.stdout.write(f"({datetime.now()}) Informing new matches...")
        non_informed_records = MatchedRecord.objects.filter(informed=False).aiterator()
        total_count = 0
        informed_count = 0
        record: MatchedRecord
        async for record in non_informed_records:
            total_count += 1
            informed = await self.match_informer.inform_match(record)
            if not informed:
                self.stdout.write(f"ERROR: Couldn't inform matched record!")
            else:
                record.informed = True
                record.save()
                informed_count += 1
        self.stdout.write(f"({datetime.now()}) Done!")
        self.stdout.write(f"{informed_count} out of {total_count} new matches have been informed to the corresponding users.")
