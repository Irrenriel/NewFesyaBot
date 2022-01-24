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
        cls.cash[uid] = Alliance(code, uid)

    @classmethod
    async def get_code(cls, uid):
        return cls.cash.get(uid).code

    @classmethod
    async def get_num_guilds(cls, uid):
        return cls.cash.get(uid).n_guilds

    @classmethod
    async def add_main(cls, uid, name, owner, n_guilds, n_peoples, b_pogs, b_money, stock, glory, row):
        cls.cash.get(uid).add_main(name, owner, n_guilds, n_peoples, b_pogs, b_money, stock, glory, row)

    @classmethod
    async def add_roster(cls, uid, roster: dict, row):
        cls.cash.get(uid).add_roster(roster, row)

    @classmethod
    async def get_data(cls, uid):
        return cls.cash.get(uid)


class Alliance:
    def __init__(self, code: str, uid: int):
        self.name = None
        self.owner = None

        self.n_guilds = None
        self.n_members = None

        self.b_pogs = None
        self.b_money = None

        self.stock = None
        self.glory = None

        self.main_row = None

        self.roster = None
        self.roster_row = None

        self.code = code
        self.uid = uid

    def add_main(self, name, owner, n_guilds, n_peoples, b_pogs, b_money, stock, glory, row):
        self.name = name
        self.owner = owner

        self.n_guilds = n_guilds
        self.n_members = n_peoples

        self.b_pogs = b_pogs
        self.b_money = b_money

        self.stock = stock
        self.glory = glory

        self.main_row = row

    def add_roster(self, roster: dict, row):
        # Saving like DICT for the future features
        self.roster = roster
        self.roster_row = row

    def get_me(self):
        return [self.code, self.name, self.owner, self.uid, self.n_members, self.n_guilds, self.b_pogs, self.b_money,
                self.stock, self.glory, ', '.join(self.roster.keys()), self.main_row, self.roster_row]

    def get_roster(self):
        return [(x, self.code) for x in self.roster]