from datetime import datetime
from typing import Optional
import threading

from async_property import async_property
from pydantic import BaseModel

from resources.tools.database import PostgreSQLDatabase
from src.content import Castles, Roles, Classes, GMRole, ROLES_DICT, GET_NEW_USER_REQUEST


class UserData(BaseModel):
    # Telegram Data
    id: int
    username: str

    # CW Data
    nickname: str
    lvl: int
    main_class: Classes
    sub_class: Classes
    guild_tag: Optional[str]
    castle: Castles

    # Bot Data
    role: Roles
    gm_role: GMRole
    hero_update: datetime


class UsersCash:
    _storage = []
    _store_by_ids = {}
    _store_by_guild_tags = {}
    _store_by_castles = {}
    _store_by_roles = {}
    _rlock = threading.RLock()

    @classmethod
    async def update(cls, db_result: list):
        """
        Updating all storages.
        :param db_result: list of Records by postgres
        """
        with cls._rlock:
            cls._storage = [UserData(**r) for r in db_result]
            await cls.reload

    @classmethod
    @async_property
    async def reload(cls):
        # Store by IDs
        if cls._store_by_ids:
            cls._store_by_ids.clear()

        # Store by Guild Tags
        if cls._store_by_guild_tags:
            cls._store_by_guild_tags.clear()

        # Store by Castles
        if cls._store_by_castles:
            cls._store_by_castles.clear()

        # Store by Roles
        if cls._store_by_roles:
            cls._store_by_roles.clear()

        # Packing
        for data in cls._storage:
            cls._store_by_ids[data.id] = data
            cls._store_by_guild_tags.setdefault(data.guild_tag, {})[data.id] = data
            cls._store_by_castles.setdefault(data.castle, {})[data.id] = data
            cls._store_by_roles.setdefault(data.role, {})[data.id] = data

    @classmethod
    async def select(cls, func) -> list:
        """
        Selecting info from stores.
        Example UsersCash().select(lambda x: x.guild_tag == 'AT' and 20 < x.lvl < 41) -> List[UserData]
        :param func: lambda logic
        :return: list of UserData
        """
        with cls._rlock:
            return list(filter(func, cls._storage))

    @classmethod
    async def select_id(cls, uids):
        """
        Selecting info from stores by ID/list of IDs.
        :param uids: uids to filter
        :return: list of UserData
        """
        with cls._rlock:
            if type(uids) is list:
                return [cls._store_by_ids.get(uid) for uid in uids]

            elif type(uids) is int:
                return cls._store_by_ids.get(uids)

    @classmethod
    async def select_castle(cls, castles) -> dict:
        """
        Selecting info from stores by Castles.
        :param castles: castles to filter
        :return: dict of UserData
        """
        with cls._rlock:
            if type(castles) is list:
                result = {}
                for i in [cls._store_by_castles.get(castle) for castle in castles]:
                    result.update(i)
                return result

            elif type(castles) is Castles:
                return cls._store_by_castles.get(castles)

    @classmethod
    async def select_guild_tag(cls, guild_tags) -> dict:
        """
        Selecting info from stores by Guild tags.
        :param guild_tags: guild tags to filter
        :return: dict of UserData
        """
        with cls._rlock:
            if type(guild_tags) is list:
                result = {}
                for i in [cls._store_by_guild_tags.get(guild_tag) for guild_tag in guild_tags]:
                    result.update(i)
                return result

            elif type(guild_tags) is str:
                return cls._store_by_guild_tags.get(guild_tags)

    @classmethod
    async def select_role(cls, roles) -> dict:
        """
        Selecting info from stores by Guild tags.
        :param roles: roles to filter
        :return: dict of UserData
        """
        with cls._rlock:
            if type(roles) is list:
                result = {}
                for i in [cls._store_by_roles.get(role) for role in roles]:
                    if not i:
                        continue
                    result.update(i)
                return result

            elif type(roles) is Roles:
                return cls._store_by_guild_tags.get(roles)

    @classmethod
    async def check_role(cls, uid: int, roles) -> bool:
        """
        Checking id to role.
        :param uid: id to check
        :param roles: roles to check
        :return: bool
        """
        with cls._rlock:
            return bool((await cls.select_role(roles)).get(uid))

    @classmethod
    async def change_role(cls, db: PostgreSQLDatabase, role: int, user: UserData):
        with cls._rlock:
            await db.execute('UPDATE users SET role = $1 WHERE id = $2', [role, user.id])

            cls._storage = list(filter(lambda x: x.id != user.id, cls._storage))
            user.role = ROLES_DICT.get(role)
            cls._storage.append(user)

            await cls.reload()

    @classmethod
    async def add_new_user(cls, db: PostgreSQLDatabase, uid: int):
        with cls._rlock:
            data = await db.fetch(GET_NEW_USER_REQUEST, [uid], one_row=True)
            data = UserData(**data)

            cls._store_by_ids[data.id] = data
            cls._store_by_guild_tags.setdefault(data.guild_tag, {})[data.id] = data
            cls._store_by_castles.setdefault(data.castle, {})[data.id] = data
            cls._store_by_roles.setdefault(data.role, {})[data.id] = data