class TempCash:
    cash = {}

    def insert(self, uid: int, mid: int):
        self.cash[uid] = mid

    def get(self, uid: int):
        return self.cash.get(uid)


class TempAllianceCash:
    cash = {}

    async def create(self, uid: int, code: str):
        self.cash[uid] = Alliance(code, uid)

    async def get_code(self, uid):
        return self.cash.get(uid).code

    async def get_num_guilds(self, uid):
        return self.cash.get(uid).n_guilds

    async def add_main(self, uid, name, owner, n_guilds, n_peoples, b_pogs, b_money, stock, glory, row):
        self.cash.get(uid).add_main(name, owner, n_guilds, n_peoples, b_pogs, b_money, stock, glory, row)

    async def add_roster(self, uid, roster: dict, row):
        alliance = self.cash.get(uid).add_roster(roster, row)

    async def get_data(self, uid):
        return self.cash.get(uid)


class Alliance:
    def __init__(self, code: str, uid: int):
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
        return [self.code, self.name, self.owner, self.uid, self.n_members, self.n_guilds, self.b_pogs, self.b_money,\
               self.stock, self.glory, ', '.join(self.roster.keys()), self.main_row, self.roster_row]

    def get_roster(self):
        return [(x, self.code) for x in self.roster]