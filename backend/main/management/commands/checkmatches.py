from django.core.management import BaseCommand

from main.matching.engine import MatchingEngine
from main.matching.match_finder.telegram_match_finder import TelegramMatchFinder
from main.matching.match_informer.telegramic_informer import TelegramicInformer


class Command(BaseCommand):
    help = 'Check if any new matches has occurred and send corresponding messages to the users.'

    def handle(self, *args, **options):
        self.stdout.write("Finding and informing matches...")
        informed_matches = MatchingEngine(TelegramMatchFinder(), TelegramicInformer()).inform_newly_matched_users()
        self.stdout.write("Done!")
        self.stdout.write(f"{len(informed_matches)} new matches have been detected and informed.")
