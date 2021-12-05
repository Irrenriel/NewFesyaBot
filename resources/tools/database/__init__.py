import sqlite3


class Database:
    def __init__(self, path_to_file: str, database_type: str, loop=None):
        """

        :param path_to_file: path to database file.
        :param database_type: type of database, available types: 'sqlite3'.
        """
        if database_type == 'sqlite3':
            self.path_to_file = path_to_file
            self.database_type = database_type
            self._con = sqlite3.connect(path_to_file)
            self.loop = loop

        else:
            raise ValueError('Wrong Database Type or path to file!')

    def _limit_check(self, limit: int) -> str:
        return f' LIMIT {limit}' if limit and type(limit) == int else ''

    async def async_check(self, request: str, args: list = None, limit: int = None):
        if args is None:
            args = []

        cur = self._con.cursor()

        if self.loop is None:
            raise ValueError('No loop!')
        res = await self.loop.run_in_executor(
            None, lambda: cur.execute(request + self._limit_check(limit), args).fetchall()
        )

        cur.close()
        return res

    def check(self, request: str, args: list = None, limit: int = None):
        if args is None:
            args = []

        cur = self._con.cursor()
        cur.execute(request + self._limit_check(limit), args)
        res = cur.fetchall()
        cur.close()
        return res