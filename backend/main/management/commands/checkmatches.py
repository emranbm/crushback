from django.core.management import BaseCommand

from main.utils.match_finder import MatchFinder


class Command(BaseCommand):
    help = 'Check if any new matches has occurred and send corresponding messages to the users.'

    def handle(self, *args, **options):
        self.stdout.write("Finding matches...")
        new_matches = MatchFinder.save_new_matched_records()
        self.stdout.write("Done!")
        self.stdout.write(f"{len(new_matches)} new matches have been saved.")
