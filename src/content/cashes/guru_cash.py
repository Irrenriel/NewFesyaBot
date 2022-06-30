import json
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime


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
