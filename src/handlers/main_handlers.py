from resources.models import dp

from resources.tools.cfilters import Command, IsUser, ChatTypeFilter
# from src.functions import start, start_new


'''<<<-----   MAIN FUNCs   ----->>>'''
# /start
dp.register_message_handler(
    start,
    Command('start'), ChatTypeFilter('private'), IsUser(is_registered=True), state='*'
)

# /start (New User)
dp.register_message_handler(
    start_new,
    Command('start'), ChatTypeFilter('private'), IsUser(is_registered=False), state='*'
    # State: None -> StateOn.Start (by if)
)
