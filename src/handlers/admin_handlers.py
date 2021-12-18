from resources.models import dp

from resources.tools.cfilters import Command, IsUser, IsReplyFilter, ChatTypeFilter, Text
from src.functions import sql, info, reg_as, activity_log, activity_log_pages


'''<<<-----   ADMIN FUNCs   ----->>>'''
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
