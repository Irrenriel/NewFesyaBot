from dataclasses import dataclass
from typing import Optional


class TempCash:
    cash = {}

    @classmethod
    def insert(cls, uid: int, mid: int):
        cls.cash[uid] = mid

    @classmethod
    def get(cls, uid: int):
        return cls.cash.get(uid)


class TempAllianceCash:
    cash = {}

    @classmethod
    async def create(cls, uid: int, code: str):
        cls.cash[uid] = Alliance(code)

    @classmethod
    async def get_code(cls, uid: int):
        return cls.cash.get(uid).code

    @classmethod
    async def get_num_guilds(cls, uid: int):
        return cls.cash.get(uid).main.n_guilds

    @classmethod
    async def add_main(cls, uid: int, *args):
        cls.cash.get(uid).main = AllianceMain(*args)


    @classmethod
    async def add_roster(cls, uid: int, roster: list, row: str):
        cls.cash.get(uid).roster = AllianceRoster(roster=roster, roster_row=row)

    @classmethod
    async def get_cash(cls, uid):
        return cls.cash.get(uid)


@dataclass
class AllianceMain:
    name: str
    owner: str

    n_guild: int
    n_members: int

    b_pogs: int
    b_money: int

    stock: int
    glory: int

    main_row: str

    def get(self):
        return self.name, self.owner, self.n_guild, self.n_members, self.b_pogs, self.b_money, self.stock, \
               self.glory, self.main_row


@dataclass
class AllianceRoster:
    roster: list
    roster_row: str

    def get(self):
        return self.roster, self.roster_row


@dataclass
class Alliance:
    code: str
    main: Optional[AllianceMain] = None
    roster: Optional[AllianceRoster] = None

    # def get_me(self):
    #     return [
    #         self.code, self.name, self.owner, self.uid,
    #         self.n_members, self.n_guilds,
    #         self.b_pogs, self.b_money, self.stock, self.glory, ', '.join(self.roster.keys()), self.main_row, self.roster_row]

    # def get_roster(self):
    #     return [(x, self.code) for x in self.roster]

    def get_me(self):
        return [
            self.code, *self.main.get(),
        ]