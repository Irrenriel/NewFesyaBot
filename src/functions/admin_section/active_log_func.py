from aiogram.types import Message, CallbackQuery
from datetime import datetime

from asyncpg import Record

from resources.tools.database import PostgreSQLDatabase
from resources.tools.keyboards import InlineKeyboard, Call
from src.content import ACTIVE_LOG_REQ_BY_USER, ACTIVE_LOG_REQ_BY_NONE
from src.content.consts.admin_dataclasses import ActiveLog


async def active_log(mes: Message, db: PostgreSQLDatabase):
    args = mes.get_args()
    if args:
        user = args[1:] if args.startswith('@') else args
        res = db.fetch(ACTIVE_LOG_REQ_BY_USER, [user])
        title = f'|🗄<b>Active Log: @{user}</b>|\n'

    else:
        user = None
        res = db.fetch(ACTIVE_LOG_REQ_BY_NONE)
        title = '|🗄<b>Active Log: General</b>|\n'

    if not res:
        await mes.answer(title + 'The Log is empty or the given user does not exist.')
        return

    pool_logs = [ActiveLog(**i) for i in res]
    len_res, txt = len(pool_logs), ''

    for row in pool_logs[:10]:
        txt += f'[<i>{datetime.fromtimestamp(row.time)}</i>] @{row.username}:\n"<code>{row.info[:20]}</code>"\n'

    page = 1
    u = user if user else 'all'

    kb = InlineKeyboard(
        Call('⬅️', f'j:{u}:{page-1}') if page - 1 else Call(' ', 'None'),
        Call(str(page), f'j:{u}:{page}'),
        Call('➡️', f'j:{u}:{page+1}') if len_res > 10 else Call(' ', 'None'),
        Call('Закрыть', 'j_cancel'),
        row_width=3
    )

    await mes.answer(title + txt, reply_markup=kb)


async def active_log_pages(call: CallbackQuery, db: PostgreSQLDatabase):
    await call.answer(cache_time=1)

    d = call.data.split(':')[1:]
    if d[0] == 'all':
        user = None
        res = db.fetch(ACTIVE_LOG_REQ_BY_NONE)
        title = '|🗄<b>Active Log: General</b>|\n'
    else:
        user = d[0]
        res = db.fetch(ACTIVE_LOG_REQ_BY_USER, [user])
        title = f'|🗄<b>Active Log: @{user}</b>|\n'

    pool_logs = [ActiveLog(**i) for i in res]
    len_res, txt = len(pool_logs), ''
    page = int(d[1])
    n = page * 10

    if res[n-10:n]:
        for row in pool_logs[n-10:n]:
            txt += f'[<i>{datetime.fromtimestamp(row.time)}</i>] @{row.username}:\n"<code>{row.info[:20]}</code>"\n'
    else:
        txt += 'The Log is empty or the given user does not exist.'

    u = user if user else 'all'

    kb = InlineKeyboard(
        Call('⬅️', f'j:{u}:{page-1}') if page - 1 else Call(' ', 'None'),
        Call(str(page), f'j:{u}:{page}'),
        Call('➡️', f'j:{u}:{page + 1}') if len_res > n else Call(' ', 'None'),
        Call('Закрыть', 'j_cancel'),
        row_width=3
    )

    await call.message.edit_text(title + txt, reply_markup=kb)


async def j_logging(mes: Message, db: PostgreSQLDatabase, db_name: str = 'active_log', info: str = None):
    id = mes.from_user.id
    username = mes.from_user.username if mes.from_user.username else mes.from_user.first_name + ':NoUsername'
    info = mes.text if info is None else info

    db.execute(,[id, username, info]
    )