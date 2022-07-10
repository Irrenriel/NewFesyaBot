import json
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from asyncpg import Record


QC_LVL_EMOJI = {1: '1️⃣', 2: '2️⃣', 3: '3️⃣', 4: '4️⃣', 5: '5️⃣', 6: '6️⃣', 7: '7️⃣'}
QC_SPEC_EMOJI = {
    'boots': '👟', 'helmet': '🧢', 'armor': '🥋', 'gloves': '🧤', 'coat': '🌂', 'shield': '🛡', 'weapon': '🗡'
}


@dataclass
class RawGuru:
    link: str
    name: str
    ownerTag: str
    ownerName: str
    ownerCastle: str
    kind: str
    mana: int
    offers: list = field(default_factory=lambda: [])
    castleDiscount: int = 0
    guildDiscount: int = 0
    specialization: defaultdict[dict] = field(default_factory=lambda: defaultdict(dict))
    qualityCraftLevel: int = 0
    specializations: defaultdict[dict] = field(default_factory=lambda: defaultdict(dict))
    maintenanceEnabled: bool = False
    maintenanceCost: int = 0
    date: datetime = datetime.now()

    def get_data(self):
        return self.link, self.name, self.ownerTag, self.ownerName, self.ownerCastle, self.kind, self.mana, \
               json.dumps(self.offers), self.castleDiscount, self.guildDiscount, json.dumps(self.specialization),\
               self.qualityCraftLevel, json.dumps(self.specializations), self.maintenanceEnabled, \
               self.maintenanceCost, self.date


@dataclass
class QCGuru:
    link: str
    name: str
    ownerTag: str
    ownerName: str
    ownerCastle: str
    mana: int
    qc_lvl: int
    spec: str
    spec_prog: int
    castleDiscount: int
    guildDiscount: int


@dataclass
class GuruData:
    link: str
    name: str
    ownertag: str
    ownername: str
    ownercastle: str
    kind: str
    mana: int
    offers: Optional[str]
    castlediscount: Optional[int]
    guilddiscount: Optional[int]
    specialization: Optional[str]
    qualitycraftlevel: Optional[int]
    specializations: Optional[str]
    maintenanceenabled: Optional[bool]
    maintenancecost: Optional[int]
    date: Optional[datetime]

    def get_guru_txt(self, owner: Record):
        specs = json.loads(self.specialization)
        offers = json.loads(self.offers)
        x = QC_LVL_EMOJI.get(self.qualitycraftlevel, '0️⃣')

        return {
            'ownerCastle': self.ownercastle,
            'ownerTag': self.ownertag,
            'ownerName': self.ownername,
            'username': '<a href="http://t.me/{}">Написать✉</a>'.format(owner['username']) if owner else 'Неизвестен',
            'qc': '\n'.join(
                [f'{x} {QC_SPEC_EMOJI.get(spec)}<code>{specs[spec]}%</code> 💧{self.mana}' for spec in specs]
            ),
            'offers': '\n'.join([f'📍{o["item"]} 💰{o["price"]} 💧{o["mana"]}' for o in offers]),
            'link': f'<a href="https://t.me/share/url?url=/ws_{self.link}">/ws_{self.link}</a>'
        }


class GuruShops:
    last_date_strftime = None
    last_date_datetime = None
    specs_cash = {'boots': [], 'armor': [], 'coat': [], 'gloves': [], 'helmet': [], 'shield': [], 'weapon': []}

    # Patterns
    P1 = '{}{}{} 💧{}'
    P2 = '<a href="https://t.me/share/url?url=/ws_{}">{}</a>'

    @classmethod
    def startup_update(cls, shops_pool: list):
        cls.specs_cash.clear()

        for i, ws in enumerate(shops_pool):
            # if ws.get('link') == 'MYdnt':
            #     print(ws)

            if isinstance(ws, Record):
                ws = dict(ws)

                if not i:
                    cls.update_callback_date(ws['date'])

                ws['specialization'] = json.loads(ws['specialization']) if ws.get('specialization') else {}
                ws['specializations'] = json.loads(ws['specializations']) if ws.get('specializations') else {}

                ws['qualityCraftLevel'] = ws.get('qualitycraftlevel')
                ws['ownerTag'] = ws.get('ownertag')
                ws['ownerName'] = ws.get('ownername')
                ws['ownerCastle'] = ws.get('ownercastle')
                ws['castleDiscount'] = ws.get('castlediscount')
                ws['guildDiscount'] = ws.get('guilddiscount')

            qc_lvl = ws.get('qualityCraftLevel')
            raw_specs = ws.get('specializations')

            if not qc_lvl or not ws.get('specialization') or 'quality_craft' not in raw_specs.keys():
                continue

            mana = ws.get('mana')
            if mana == 0:
                continue

            # Dict of Guru Spec
            specs_dict = raw_specs.get('quality_craft', {}).get('Values', {})

            for sp in specs_dict.items():
                spec, spec_prog = sp
                if spec_prog != 100:
                    continue

                cls.specs_cash.setdefault(spec, []).append(
                    QCGuru(
                        ws['link'], ws['name'], ws['ownerTag'], ws['ownerName'], ws['ownerCastle'], ws['mana'],
                        qc_lvl, spec, spec_prog, ws.get('castleDiscount', 0), ws.get('guildDiscount', 0)
                    )
                )

    @classmethod
    def get_last_date_strftime(cls):
        return cls.last_date_strftime

    @classmethod
    def get_last_date_datetime(cls):
        return cls.last_date_datetime

    @classmethod
    def update_callback_date(cls, date: datetime):
        cls.last_date_strftime = date.strftime('%Y-%m-%d %H:%M:%S')
        cls.last_date_datetime = date

    @classmethod
    def get_specs_cash(cls):
        return cls.specs_cash

    @classmethod
    def update_specs_cash(cls, specs_cash: dict):
        cls.specs_cash = specs_cash

    @classmethod
    def ws_shops_formatter(cls, gurus: List[QCGuru]):
        return '\n'.join(
            [
                cls.P1.format(
                    QC_LVL_EMOJI[g.qc_lvl], g.ownerCastle, cls.P2.format(g.link, g.ownerName), str(g.mana)
                ) for g in sorted(gurus, key=lambda g: -g.qc_lvl)
            ]
        ) if gurus else '...'

    @classmethod
    def get_specs_cash_ws_cmd(cls):
        x = {k: cls.ws_shops_formatter(v) for k, v in cls.specs_cash.items()}
        x['date'] = cls.last_date_strftime if cls.last_date_strftime else '...'
        return x
