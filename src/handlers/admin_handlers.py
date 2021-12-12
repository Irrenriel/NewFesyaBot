from resources.models import dp

from resources.tools.cfilters import Command, IsUser, IsReplyFilter
from src.functions import sql, info, reg_as


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
