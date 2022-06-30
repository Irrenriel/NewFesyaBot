from logging import info

from resources.tools.database import PostgreSQLDatabase
from .banned_cash import BannedUsersCash
from .temp_cash import TempCash, TempAllianceCash
from .users_cash import UsersCash, UserData
from .adv_users_cash import AdvUsersCash, AdvUserData
from .. import MAIN_REQ, ADV_MAIN_REQ, BANNED_MAIN_REQ


async def installing_cashes(db: PostgreSQLDatabase):
    await UsersCash.update(await db.fetch(MAIN_REQ))
    info('▻ UsersCash was updated!')

    await AdvUsersCash.update(await db.fetch(ADV_MAIN_REQ))
    info('▻ AdvUsersCash was updated!')

    await BannedUsersCash.update(await db.fetch(BANNED_MAIN_REQ))
    info('▻ BannedUsersCash was updated !')
