from typing import List

from asgiref.sync import sync_to_async

from main.matching.match_finder.base import MatchFinder
from main.matching.match_informer.base import MatchInformer
from main.models import MatchedRecord


class MatchingEngine:
    def __init__(self, match_finder: MatchFinder, match_informer: MatchInformer):
        self.match_finder = match_finder
        self.match_informer = match_informer

    async def inform_newly_matched_users(self) -> List[MatchedRecord]:
        """

        :return: Informed matched records
        """
        new_matches = await self.match_finder.save_new_matched_records()
        informed_records: List[MatchedRecord] = []
        for matched_record in new_matches:
            informed = await self.match_informer.inform_match(matched_record)
            if informed:
                matched_record.informed = True
                await sync_to_async(matched_record.save)()
                informed_records.append(matched_record)
        return informed_records
