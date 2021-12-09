import asyncpg


class PostgreSQLDatabase:
    def __init__(self, session_name: str,  user: str, password: str, database: str, host: str):
        self._pool = None
        self._session_name = session_name
        self._user = user
        self._password = password
        self._database = database
        self._host = host

    async def connect(self):
        """
        Connecting to database by arguments as a pool.
        :param user: user in database
        :param password: password to access database
        :param database: name of table
        :param host: IP host
        """
        self._pool: asyncpg.Pool = await asyncpg.create_pool(
            user=self._user,
            password=self._password,
            database=self._database,
            host=self._host
        )
        return True

    async def fetch(self, request: str, args: list[str] = None, one_row: bool = False) -> \
            list[asyncpg.Record] | asyncpg.Record | None:
        """
        Get a data rows from database by request.
        :param request: SQL request
        :param args: Args to insert into SQL request
        :param one_row: bool - True if you need to get 1 data row, False (default) if you need to get all data rows
        :return: Data rows if all is ok, else Exception
        """
        if args is None:
            args = []

        async with self._pool.acquire() as conn:
            # Get One Row
            if one_row:
                result = await conn.fetchrow(request, *args)
                return result

            # Get All Rows
            else:
                result: list[asyncpg.Record] = await conn.fetch(request, *args)
                return result

    async def execute(self, request: str,  args: list[str] = None):
        """
        Execute a request to database.
        :param request: SQL request
        :param args: Args to insert into SQL request
        :return: bool - True is ok, False is fail
        """
        if args is None:
            args = []

        async with self._pool.acquire() as conn:
            await conn.execute(request, *args)

    async def disconnect(self):
        """
        Disconnect from database.
        """
        await self._pool.close()
