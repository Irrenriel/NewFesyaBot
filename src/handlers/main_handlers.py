from config import CW_BOT_ID
from resources.models import dp

from resources.tools.cfilters import Command, IsUser, ChatTypeFilter, Text, IsForward
from resources.tools.states import StateOn
from src.functions import start, hero_insert, start_new

'''<<<-----   MAIN FUNCs   ----->>>'''
# /start
dp.register_message_handler(
    start,
    Command('start'), ChatTypeFilter('private'), IsUser(is_registered=True), state='*'
)

# 🗳Меню, Вернуться↩
dp.register_message_handler(
    start,
    Text(['🗳Меню', 'Вернуться↩']), ChatTypeFilter('private'), IsUser(is_registered=True), state='*'
)

# /start (New User)
dp.register_message_handler(
    start_new,
    Command('start'), ChatTypeFilter('private'), IsUser(is_registered=False), state='*'
    # State: None -> StateOn.Registration
)

# From CW /hero Inputer For Registration
dp.register_message_handler(
    hero_insert,
    ChatTypeFilter('private'), state=StateOn.Registration
    # State: StateOn.Registration -> None
)

# From CW /hero Inputer For Update
dp.register_message_handler(
    hero_insert,
    Text(contains="🎉Достижения: /ach"), IsForward(CW_BOT_ID), IsUser(is_registered=True)
)
