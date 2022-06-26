from aiogram.types import Message, CallbackQuery

from resources.tools.database import PostgreSQLDatabase
from resources.tools.keyboards import InlineKeyboard, Call
from src.content import ACTIVITY_LOGGING_REQ_BY_USER, ACTIVITY_LOGGING_REQ_BY_NONE
from src.content.consts.admin_dataclasses import ActiveLog


async def activity_log(mes: Message, db: PostgreSQLDatabase):
    # Get target (user) for journal and create start row
    args = mes.get_args()
    if args:
        user = args[1:] if args.startswith('@') else args
        res = await db.fetch(ACTIVITY_LOGGING_REQ_BY_USER, [user])
        title = f'|🗄<b>Active Log: @{user}</b>|\n'

    else:
        user = None
        res = await db.fetch(ACTIVITY_LOGGING_REQ_BY_NONE)
        title = '|🗄<b>Active Log: General</b>|\n'

    # If journal is empty
    if not res:
        await mes.answer(title + 'The Log is empty or the given user does not exist.')
        return

    # Formatting logs to array
    pool_logs = [ActiveLog(**i) for i in res]
    len_res, txt = len(pool_logs), ''

    for row in pool_logs[:10]:
        txt += f'[<i>{row.time.strftime("%H:%M:%S")}</i>] @{row.username}:\n"<code>{row.data[:20]}</code>"\n'

    page = 1
    u = user if user else 'all'

    # Creating keyboard
    _1st_btn = Call("⬅️", f"j:{u}:{page-1}") if page - 1 else Call(" ", "None")
    _3rd_btn = Call("➡️", f"j:{u}:{page+1}") if len_res > 10 else Call(" ", "None")
    kb = InlineKeyboard(
        Call("⬅️", f"j:{u}:{page-1}") if page - 1 else Call(" ", "None"),
        Call(str(page), f"j:{u}:{page}"),
        Call("➡️", f"j:{u}:{page+1}") if len_res > 10 else Call(" ", "None"),
        Call("Закрыть", "j_cancel"), row_width=3
    )

    await mes.answer(title + txt, reply_markup=kb)


async def activity_log_pages(call: CallbackQuery, db: PostgreSQLDatabase):
    await call.answer(cache_time=1)

    d = call.data.split(':')[1:]
    if d[0] == 'all':
        user = None
        res = await db.fetch(ACTIVITY_LOGGING_REQ_BY_NONE)
        title = '|🗄<b>Active Log: General</b>|\n'
    else:
        user = d[0]
        res = await db.fetch(ACTIVITY_LOGGING_REQ_BY_USER, [user])
        title = f'|🗄<b>Active Log: @{user}</b>|\n'

    pool_logs = [ActiveLog(**i) for i in res]
    len_res, txt = len(pool_logs), ''
    page = int(d[1])
    n = page * 10

    if res[n-10:n]:
        for row in pool_logs[n-10:n]:
            txt += f'[<i>{row.time.strftime("%H:%M:%S")}</i>] @{row.username}:\n"<code>{row.data[:20]}</code>"\n'
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


# async def pager(slice: int = 10):
#     n_slice = 10
#
#
#
#
# async def create_pager_kb(n_slice: int, page: int, results: list, u: str):
#     _1st_btn = Call("◀️", f'j:{u}:{page-1}') if page - 1 else Call(" ", "None")
#     _2nd_btn = Call(str(page), f'j:{u}:{page}')
#     _3rd_btn = Call("▶️", f'j:{u}:{page-1}') if len(results) > page * n_slice else Call(" ", "None")
#     return InlineKeyboard(_1st_btn, _2nd_btn, _3rd_btn, Call('Закрыть', 'j_cancel'), row_width=3)
