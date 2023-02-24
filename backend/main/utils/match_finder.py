import logging
from typing import Iterable, List

from django.core.exceptions import ValidationError

from main.models import MatchedRecord, User, Crush

logger = logging.getLogger(__name__)


class MatchFinder:
    @staticmethod
    def save_new_matched_records() -> List[MatchedRecord]:
        user_ids = {
            u[1]: u[0]
            for u in User.objects.values_list('id', 'telegram_username')
        }
        crushes: Iterable[Crush] = Crush.objects.all()
        new_matches: List[MatchedRecord] = []
        for crush in crushes:
            crush_user_id = user_ids.get(crush.telegram_username)
            if crush_user_id is not None:
                try:
                    new_matches.append(MatchedRecord.create_new_match(crush_user_id, crush.crusher_id))
                except ValidationError as e:
                    logger.debug(f"MatchedRecord for users {crush_user_id} and {crush.crusher_id} already exists.\n"
                                 f"Validation error: {e}")
        return new_matches
