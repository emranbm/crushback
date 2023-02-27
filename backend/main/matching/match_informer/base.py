from abc import ABC, abstractmethod

from main.models import MatchedRecord


class MatchInformer(ABC):
    @abstractmethod
    async def inform_match(self, matched_record: MatchedRecord) -> bool:
        """

        :param matched_record:
        :return: True if the users are successfully informed. Otherwise False.
        """
        pass
