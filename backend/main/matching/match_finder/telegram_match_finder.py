import logging
from typing import List

from asgiref.sync import sync_to_async
from django.core.exceptions import ValidationError
from django.db import connection
from django.db.backends.utils import CursorWrapper

from main.matching.match_finder.base import MatchFinder
from main.models import MatchedRecord, User, Crush
from main.utils.db_utils import get_table_name, get_column_name as col

logger = logging.getLogger(__name__)


class TelegramMatchFinder(MatchFinder):
    async def save_new_matched_records(self) -> List[MatchedRecord]:
        return await sync_to_async(self._save_new_matched_records)()

    def _save_new_matched_records(self) -> List[MatchedRecord]:
        with connection.cursor() as cursor:
            cursor: CursorWrapper
            cursor.execute(f"SELECT user1.id, user2.id "
                           f"FROM {get_table_name(User)} AS user1 "
                           f"INNER JOIN {get_table_name(Crush)} AS user1_crush "
                           f"ON user1.id = user1_crush.{col(Crush.crusher)} "
                           f"INNER JOIN {get_table_name(User)} AS user2 "
                           f"ON user1_crush.{col(Crush.telegram_username)} = user2.{col(User.telegram_username)} "
                           f"INNER JOIN {get_table_name(Crush)} AS user2_crush "
                           f"ON user2_crush.{col(Crush.crusher)} = user2.id "
                           f"WHERE user1_crush.{col(Crush.telegram_username)} = user2.{col(User.telegram_username)} "
                           f"  AND user2_crush.{col(Crush.telegram_username)} = user1.{col(User.telegram_username)} ")
            matches = cursor.fetchall()
            new_matches: List[MatchedRecord] = []
            for user_id_1, user_id_2 in matches:
                try:
                    new_matches.append(MatchedRecord.create_new_match(user_id_1, user_id_2))
                except ValidationError as e:
                    logger.debug(f"MatchedRecord for users {user_id_1} and {user_id_2} already exists.\n"
                                 f"Validation error: {e}")
        return new_matches
