from logging import info

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
        info('▻ Database connected!')

    async def fetch(self, request: str, args: list = None, one_row: bool = False):
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
                result = await conn.fetch(request, *args)
                return result

    async def execute(self, request: str, args: list = None, many: bool = False):
        """
        Execute a request to database.
        :param request: SQL request
        :param args: Args to insert into SQL request
        :param many: True if you need to user executemany, else False
        :return: bool - True is ok, False is fail
        """
        if args is None:
            args = []

        async with self._pool.acquire() as conn:
            if many:
                await conn.executemany(request, args)
            else:
                await conn.execute(request, *args)

    async def fetch_orm(
            self, model, req_or_records: Union[str, List], *args, one_row: bool = False
    ):
        """
        Get the results of the database unpacked into the dataclass of the model
        :param model: dataclass model to unpack records
        :param req_or_records: list of fetch records or str request for fetch
        :param args: list of args (if req_or_args is sql request)
        :param one_row: True to get only one record (if req_or_args is sql request)
        :return: model or list of models
        """
        if isinstance(req_or_records, str):
            req_or_records = await self.fetch(req_or_records, *args, one_row=one_row)

        if not isinstance(req_or_records, List) and not isinstance(req_or_records, Record):
            raise ValueError('Variable req_or_records must be a sql string request or list of results!')

        if isinstance(req_or_records, Record):
            return model(**req_or_records)

        else:
            return [model(**i) for i in req_or_records]

    async def disconnect(self):
        """
        Disconnect from database.
        """
        await self._pool.close()
