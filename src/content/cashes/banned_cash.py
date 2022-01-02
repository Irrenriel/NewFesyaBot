import threading


class BannedUsersCash:
    _storage = []
    _rlock = threading.RLock()

    async def update(self, db_result: list):
        """
        Updating all storages.
        :param db_result: list of Records by postgres
        """
        with BannedUsersCash._rlock:
            self._storage = [r.get('id') for r in db_result]

    async def get_storage(self):
        with BannedUsersCash._rlock:
            return self._storage