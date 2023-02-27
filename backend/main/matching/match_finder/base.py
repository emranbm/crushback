from abc import ABC, abstractmethod
from typing import List

from main.models import MatchedRecord


class MatchFinder(ABC):
    @abstractmethod
    async def save_new_matched_records(self) -> List[MatchedRecord]:
        pass
