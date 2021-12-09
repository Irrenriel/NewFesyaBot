from dataclasses import dataclass
from asyncpg import Record

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
    storage = []
    store_by_ids = {}
    store_by_guild_tags = {}
    store_by_castles = {}
    store_by_roles = {}

    async def reset(self, db_result: list[Record]):
        self.storage = [UserData(**r) for r in db_result]

        # Store by ID
        if self.store_by_ids:
            self.store_by_ids.clear()

        # Store by Guild Tags
        if self.store_by_guild_tags:
            self.store_by_guild_tags.clear()

        # Store by Castles
        if self.store_by_castles:
            self.store_by_castles.clear()

        # Store by Roles
        if self.store_by_roles:
            self.store_by_roles.clear()