import threading
from pydantic import BaseModel


class AdvUserData(BaseModel):
    # Telegram Data
    id: int

    # Adv Progress
    rank: int
    reputation: int

    # Adv Quests
    avail_quests: int
    inprog_quest: int
    d_limit: int


class AdvUsersCash:
    _storage = []
    _store_by_ids = {}
    _store_by_ranks = {}

    _rlock = threading.RLock()

    async def update(self, db_result: list):
        """
        Updating all storages.
        :param db_result: list of Records by postgres
        """
        with AdvUsersCash._rlock:
            self._storage = [AdvUserData(**r) for r in db_result]

            # Store by IDs
            if self._store_by_ids:
                self._store_by_ids.clear()

            # Store by Ranks
            if self._store_by_ranks:
                self._store_by_ranks.clear()

            # Packing
            for data in self._storage:
                self._store_by_ids[data.id] = data
                self._store_by_ranks.setdefault(data.rank, {})[data.id] = data

    async def select(self, func) -> list:
        """
        Selecting info from stores.
        Example AdvUsersCash().select(lambda x: x.id == 1234567 and 2 < x.rank < 3) -> List[AdvUserData]
        :param func: lambda logic
        :return: list of AdvUserData
        """
        with AdvUsersCash._rlock:
            return list(filter(func, self._storage))

    async def select_id(self, uids) -> list:
        """
        Selecting info from stores by ID/list of IDs.
        :param uids: uids to filter
        :return: list of AdvUserData
        """
        with AdvUsersCash._rlock:
            if type(uids) is list:
                return [self._store_by_ids.get(uid) for uid in uids]

            elif type(uids) is int:
                return self._store_by_ids.get(uids)

    async def select_rank(self, ranks) -> dict:
        """
        Selecting info from stores by Ranks.
        :param ranks: ranks to filter
        :return: list of AdvUserData
        """
        with AdvUsersCash._rlock:
            if type(ranks) is list:
                result = {}
                for i in [self._store_by_ranks.get(rank) for rank in ranks]:
                    result.update(i)
                return result

            elif type(ranks) is int:
                return self._store_by_ranks.get(ranks)