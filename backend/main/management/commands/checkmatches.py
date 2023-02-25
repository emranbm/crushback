from django.core.management import BaseCommand

from main.matching.match_finder.telegram_match_finder import TelegramMatchFinder


class Command(BaseCommand):
    help = 'Check if any new matches has occurred and send corresponding messages to the users.'

    def handle(self, *args, **options):
        self.stdout.write("Finding matches...")
        new_matches = TelegramMatchFinder().save_new_matched_records()
        self.stdout.write("Done!")
        self.stdout.write(f"{len(new_matches)} new matches have been saved.")
