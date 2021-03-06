from aiogram import Dispatcher

from resources.tools.cfilters import Command, IsUser, IsReplyFilter, Text
from src.functions import sql, info, reg_as, activity_log, activity_log_pages, callback_cancel, callback_none, ban, \
    unban, update_cashes


async def register_admin_handlers(dp: Dispatcher):
    """
    Registration ADMIN handlers.
    :param dp: aiogram Dispatcher
    :return:
    """
    # /sql
    dp.register_message_handler(
        sql,
        Command('sql'), IsUser(is_admin=True)
    )

    # /inf
    dp.register_message_handler(
        info,
        Command('inf'), IsReplyFilter('is_reply'), IsUser(is_admin=True)
    )

    # /reg_as
    dp.register_message_handler(
        reg_as,
        Command('reg_as'), IsReplyFilter('is_reply'), IsUser(is_admin=True)
    )

    # /ban
    dp.register_message_handler(
        ban,
        Command('ban'), IsUser(is_admin=True)
    )

    # /ban
    dp.register_message_handler(
        unban,
        Command('unban'), IsUser(is_admin=True)
    )

    # /j (Journal)
    dp.register_message_handler(
        activity_log,
        Command('j'), IsUser(is_admin=True)
    )

    # Switch Pages (Journal)
    dp.register_callback_query_handler(
        activity_log_pages,
        Text(startswith='j:'), IsUser(is_admin=True)
    )

    # Cancel (Journal)
    dp.register_callback_query_handler(
        callback_cancel,
        Text('j_cancel'), IsUser(is_admin=True)
    )

    # Update Cashes
    dp.register_message_handler(
        update_cashes,
        Command('update_cash'), IsUser(is_admin=True)
    )

    # SETTINGS
    # None Callbacks
    dp.register_callback_query_handler(
        callback_none,
        Text('None')
    )

    # Close Callbacks
    dp.register_callback_query_handler(
        callback_cancel,
        Text('cancel')
    )
