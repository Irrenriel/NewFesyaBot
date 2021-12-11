from dataclasses import dataclass
from asyncpg import Record
import threading

from src.content import Castles, Roles, Classes


@dataclass
class UserData:
    # Telegram Data
    id: int
    username: str

    # CW Data
    nickname: str
    lvl: int
    main_class: Classes
    sub_class: Classes
    guild_tag: str
    castle: Castles

    # Bot Data
    role: Roles
    last_hero_update: int
    gm_role: int


class UsersCash:
    _storage = []
    _store_by_ids = {}
    _store_by_guild_tags = {}
    _store_by_castles = {}
    _store_by_roles = {}
    _rlock = threading.RLock()

    async def update(self, db_result: list[Record]):
        with UsersCash._rlock:
            self._storage = [UserData(**r) for r in db_result]

            # Store by ID
            if self._store_by_ids:
                self._store_by_ids.clear()

            # Store by Guild Tags
            if self._store_by_guild_tags:
                self._store_by_guild_tags.clear()

            # Store by Castles
            if self._store_by_castles:
                self._store_by_castles.clear()

            # Store by Roles
            if self._store_by_roles:
                self._store_by_roles.clear()

            # Packing
            for data in self._storage:
                self._store_by_ids[data.id] = data
                self._store_by_guild_tags.setdefault(data.guild_tag, {})[data.id] = data
                self._store_by_castles.setdefault(data.castle, {})[data.id] = data
                self._store_by_roles.setdefault(data.role, {})[data.id] = data
            print(self._store_by_castles)

    async def select(self, func) -> list:
        """
        Selecting info from stores.
        Example UsersCash().select(lambda x: x.guild_tag == 'AT' and 20 < x.lvl < 41) -> List[UserData]
        :param func: lambda logic
        :return: list of UserData
        """
        with UsersCash._rlock:
            return list(filter(func, self._storage))

    async def select_id(self, uids: list[int] | int) -> list:
        """
        Selecting info from stores by ID/list of IDs.
        :param uids: uids to filter
        :return: list of UserData
        """
        with UsersCash._rlock:
            if type(uids) is list:
                return [self._store_by_ids.get(uid) for uid in uids]

            elif type(uids) is int:
                return [self._store_by_ids.get(uids)]

    async def select_castle(self, castles: list[Castles] | Castles) -> dict:
        """
        Selecting info from stores by Castles.
        :param castles: castles to filter
        :return: dict of UserData
        """
        with UsersCash._rlock:
            if type(castles) is list:
                result = {}
                for i in [self._store_by_castles.get(castle) for castle in castles]:
                    result.update(i)
                return result

            elif type(castles) is Castles:
                return self._store_by_castles.get(castles)

    async def select_guild_tag(self, guild_tags: list[str] | str) -> dict:
        """
        Selecting info from stores by Guild tags.
        :param guild_tags: guild tags to filter
        :return: dict of UserData
        """
        with UsersCash._rlock:
            if type(guild_tags) is list:
                result = {}
                for i in [self._store_by_guild_tags.get(guild_tag) for guild_tag in guild_tags]:
                    result.update(i)
                return result

            elif type(guild_tags) is str:
                return self._store_by_guild_tags.get(guild_tags)

    async def select_role(self, roles: list[Roles] | Roles) -> dict:
        """
        Selecting info from stores by Guild tags.
        :param roles: roles to filter
        :return: dict of UserData
        """
        with UsersCash._rlock:
            if type(roles) is list:
                result = {}
                for i in [self._store_by_roles.get(role) for role in roles]:
                    result.update(i)
                return result

            elif type(roles) is Roles:
                return self._store_by_guild_tags.get(roles)

    async def check_role(self, uid: int, roles: Roles | list[Roles]) -> bool:
        """
        Checking id to role.
        :param uid: id to check
        :param roles: roles to check
        :return: bool
        """
        return bool((await self.select_role(roles)).get(uid))