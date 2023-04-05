from django.db import connection
from django.db.backends.utils import CursorWrapper
from django.test import TestCase

from main import testing_utils
from main.data_migrations.telegram_username_lowercase import Migration
from main.models import User, Crush
from main.utils.db_utils import get_table_name


class MigrationTest(TestCase):
    @staticmethod
    def _run_sql(query: str) -> None:
        with connection.cursor() as cursor:
            cursor: CursorWrapper
            cursor.execute(query)

    def test_should_make_crush_and_user_telegram_usernames_lower(self):
        user, crush = testing_utils.create_user_and_their_crush("user", "crush")
        self._run_sql(f"UPDATE {get_table_name(User)} SET telegram_username = 'uSEr' WHERE id = '{user.pk}'")
        self._run_sql(f"UPDATE {get_table_name(Crush)} SET telegram_username = 'cRUSH' WHERE id = '{crush.pk}'")
        user.refresh_from_db()
        crush.refresh_from_db()
        self.assertEqual("uSEr", user.telegram_username)
        self.assertEqual("cRUSH", crush.telegram_username)

        Migration().migrate()

        user.refresh_from_db()
        crush.refresh_from_db()
        self.assertEqual("user", user.telegram_username)
        self.assertEqual("crush", crush.telegram_username)
