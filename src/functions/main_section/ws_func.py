# /shops
from aiogram.types import Message

from resources.tools.database import PostgreSQLDatabase
from src.content import GURU_SHOPS_TEXT, GET_WS_LINK_SHOP, GURU_OWNER_TEXT
from src.content.cashes.guru_cash import GuruShops, GuruData


async def ws_shops(mes: Message):
    await mes.answer(GURU_SHOPS_TEXT.format(**GuruShops.get_specs_cash_ws_cmd()))


async def ws_owners(mes: Message, regexp_command, db: PostgreSQLDatabase):
    rec = await db.fetch(GET_WS_LINK_SHOP, [regexp_command.group(1)], one_row=True)
    if not rec:
        return

    guru = GuruData(**rec)
    owner = await db.fetch('SELECT username FROM ws_owners WHERE link = $1', [guru.link], one_row=True)

    await mes.answer(GURU_OWNER_TEXT.format(**guru.get_guru_txt(owner)), disable_web_page_preview=True)
