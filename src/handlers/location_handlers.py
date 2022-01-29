from config import config
from resources.models import dp

from resources.tools.cfilters import Command, IsUser, Text, IsForward
from src.content import Roles
from src.functions import new_location_input, new_bless_input, new_res_input, loc_del, loc_info, loc_history, \
    loc_capture, loc_miss, loc_buffs, loc_list, callback_cancel, loc_list_objects, loc_list_map, loc_help, loc_check, \
    loc_resurrect

'''<<<-----   LOCATION SECTION   ----->>>'''
# New Location Input
dp.register_message_handler(
    new_location_input,
    Text(contains="То remember the route you associated it with simple combination:"), IsForward(config.CW_BOT_ID)
)

# Location`s Bless Input
dp.register_message_handler(
    new_bless_input,
    Text(contains="attractions:"), IsForward(config.CW_BOT_ID),
    IsUser(has_roles=[Roles.ADMIN, Roles.ALLIANCE_LEADER, Roles.COMMANDER, Roles.OFFICER])
)

# Location`s Resource Input
dp.register_message_handler(
    new_res_input,
    Text(startswith='🤝 Your alliance.'), IsForward(config.CW_BOT_ID),
    IsUser(has_roles=[Roles.ADMIN, Roles.ALLIANCE_LEADER, Roles.COMMANDER, Roles.OFFICER])
)

# Delete Location from Database, /l_del [code]
dp.register_message_handler(
    loc_del,
    Command('l_del'), IsUser(has_roles=[Roles.ADMIN, Roles.ALLIANCE_LEADER])
)

# Resurrect Location from Grave :), /l_resurrect [code]
dp.register_message_handler(
    loc_resurrect,
    Command('l_resurrect'), IsUser(has_roles=Roles.ADMIN)
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

# Check Captured Locations List, /l_capture [code]
dp.register_message_handler(
    loc_capture,
    Command('l_capture'), IsUser(has_roles=[Roles.ADMIN, Roles.ALLIANCE_LEADER, Roles.COMMANDER, Roles.OFFICER])
)

# Check Missing Locations List, /l_miss
dp.register_message_handler(
    loc_miss,
    Command('l_miss'), IsUser(is_registered=True)
)

# Check List of Buffs, /l_buffs
dp.register_message_handler(
    loc_buffs,
    Command('l_buffs'), IsUser(has_roles=[Roles.ADMIN, Roles.ALLIANCE_LEADER, Roles.COMMANDER, Roles.OFFICER])
)

# List of Locations, /l_list
dp.register_message_handler(
    loc_list,
    Command('l_list'), IsUser(is_registered=True)
)

# 'Меню' button
dp.register_callback_query_handler(
    loc_list,
    Text('ll:menu'), IsUser(is_registered=True)
)

# 'Закрыть' button
dp.register_callback_query_handler(
    callback_cancel,
    Text('ll:cancel'), IsUser(is_registered=True)
)

# 🚩Карта
dp.register_callback_query_handler(
    loc_list_map,
    Text(startswith='ll:map:'), IsUser(is_registered=True)
)

# 🏷Руины, 📦Шахты, 🎖Форты
dp.register_callback_query_handler(
    loc_list_objects,
    Text(startswith='ll:'), IsUser(is_registered=True)
)

# Checking locations on existing, /l_check, /l_chk
dp.register_message_handler(
    loc_check,
    Command(['l_check', 'l_chk']), IsUser(has_roles=[Roles.ADMIN, Roles.ALLIANCE_LEADER, Roles.COMMANDER])
)

# Help for this section`s commands
dp.register_message_handler(
    loc_help,
    Command('l_help'), IsUser(is_registered=True)
)
