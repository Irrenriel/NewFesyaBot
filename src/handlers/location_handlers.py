from config import CW_BOT_ID
from resources.models import dp

from resources.tools.cfilters import Command, IsUser, ChatTypeFilter, Text, IsForward
from src.content import Roles
from src.functions import new_location_input, new_bless_input, new_res_input, loc_del, loc_info

'''<<<-----   LOCATION SECTION   ----->>>'''
# New Location Input
dp.register_message_handler(
    new_location_input,
    Text(contains="То remember the route you associated it with simple combination:"), IsForward(CW_BOT_ID)
)

# Location`s Bless Input
dp.register_message_handler(
    new_bless_input,
    Text(contains="attractions:"), IsForward(CW_BOT_ID),
    IsUser(has_roles=[Roles.ADMIN, Roles.ALLIANCE_LEADER, Roles.COMMANDER, Roles.OFFICER])
)

# Location`s Resource Input
dp.register_message_handler(
    new_res_input,
    Text(startswith='🤝 Your alliance.'), IsForward(CW_BOT_ID),
    IsUser(has_roles=[Roles.ADMIN, Roles.ALLIANCE_LEADER, Roles.COMMANDER, Roles.OFFICER])
)

# Delete Location from Database, /l_del [code]
dp.register_message_handler(
    loc_del,
    Command('l_del'), IsUser(has_roles=[Roles.ADMIN, Roles.ALLIANCE_LEADER])
)

# Check Info about Location, /l_info [name/code]
dp.register_message_handler(
    loc_info,
    Command('l_info'), IsUser(has_roles=[Roles.ADMIN, Roles.ALLIANCE_LEADER, Roles.COMMANDER, Roles.OFFICER])
)

# Check History of Location, /l_history [code]
dp.register_message_handler(
    loc_history,
    Command('l_history'), IsUser(has_roles=[Roles.ADMIN, Roles.ALLIANCE_LEADER, Roles.COMMANDER, Roles.OFFICER])
)