import threading

from async_property import async_property


class BannedUsersCash:
    _storage = []
    _rlock = threading.RLock()

    @classmethod
    async def update(cls, db_result: list):
        """
        Updating all storages.
        :param db_result: list of Records by postgres
        """
        with cls._rlock:
            cls._storage = [r.get('id') for r in db_result]

    @classmethod
    @async_property
    async def get_storage(cls):
        with cls._rlock:
            return cls._storage