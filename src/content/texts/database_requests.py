MAIN_REQ = """
SELECT id, username, nickname, lvl, main_class, sub_class, guild_tag, castle, role, gm_role, hero_update FROM users;
"""

ADV_MAIN_REQ = "SELECT id, rank, reputation, avail_quests, inprog_quest, d_limit FROM adv_users;"

BANNED_MAIN_REQ = 'SELECT id FROM banned_users;'

ACTIVITY_LOGGING_REQ_BY_USER = """
SELECT id, username, data, time, date FROM activity_logger_fesya
WHERE username = $1 ORDER BY date DESC;
"""

ACTIVITY_LOGGING_REQ_BY_NONE = "SELECT id, username, data, time, date FROM activity_logger_fesya ORDER BY date DESC;"

ACTIVITY_LOGGING_REQ_INSERT = "INSERT INTO activity_logger_fesya (id, username, data) VALUES ($1, $2, $3);"

REG_NEW_USER_REQ = """
INSERT INTO users (id, username, nickname, lvl, main_class, sub_class, guild_tag, castle)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8);
"""

UPDATE_USER_REQ = """UPDATE users SET username = $1, nickname = $2, lvl = $3, main_class = $4, sub_class = $5, 
guild_tag = $6, castle = $7, hero_update = LOCALTIMESTAMP WHERE id = $8"""

GET_NEW_USER_REQUEST = """
SELECT id, username, nickname, lvl, main_class, sub_class, guild_tag, castle, role, gm_role, hero_update
FROM users WHERE id = $1;
"""

AL_GET_ALLIANCE_BY_GUILD_REQ = '''
SELECT alliance_hq.al_name, alliance_hq.al_code, alliance_hq.al_owner, users.username as al_leader_username,
alliance_hq.n_members, alliance_hq.n_guilds, alliance_hq.al_guilds, alliance_hq.al_main_last_update,
alliance_hq.al_rost_last_update, alliance_hq.al_leader
FROM alliance_guilds
INNER JOIN alliance_hq ON alliance_guilds.al_code = alliance_hq.al_code
INNER JOIN users ON alliance_hq.al_leader = users.id
WHERE alliance_guilds.guild_tag = $1
'''

REG_NEW_ALLIANCE = '''
INSERT INTO alliance_hq (
    al_code, al_leader, al_name, n_guilds, n_members, al_owner, al_balance_pogs, al_balance_money, al_stock,
    al_glory, al_guilds, al_main_raw, al_roster_raw
) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
'''

REG_GUILDS_TO_ALLIANCE = '''
INSERT INTO alliance_guilds (al_code, guild_tag)
VALUES ($1, $2)
ON CONFLICT (guild_tag) DO UPDATE SET al_code = $1
'''

GET_GUILDS_INFO_FOR_PERC = '''
SELECT guild_tag, g_main_raw, g_roster_raw, g_atklist_raw, g_deflist_raw,
main_last_upd, roster_last_upd, atklist_last_upd, deflist_last_upd
FROM alliance_guilds WHERE guild_tag = any($1::text[])
'''

INCREASE_LOCATION_TOP_COUNT_REQ = '''
INSERT INTO location_top (uid) VALUES ($1) ON CONFLICT (uid) DO UPDATE SET count = location_top.count + 1
'''

INSERT_OR_UPDATE_LOCATION_BUFF_REQ = '''
INSERT INTO loc_buff (code, bless_json) VALUES ($1, $2) ON CONFLICT (code) DO UPDATE SET bless_json = $2
'''

INSERT_OR_UPDATE_LOCATION_RES_REQ = '''
INSERT INTO loc_res (code, res_json) VALUES ($1, $2) ON CONFLICT (code) DO UPDATE SET res_json = $2
'''

LOC_HISTORY_REQ = 'SELECT date, url, txt FROM loc_history WHERE code = $1 ORDER BY -url LIMIT $2'

LOC_CAPTURE_REQ = '''
SELECT code, name, lvl, type, conqueror, cycle, status FROM loc WHERE conqueror = $1 and exist = True ORDER BY lvl
'''

LOC_INFO_REQ = 'SELECT code, name, lvl, type, conqueror, cycle, status FROM loc WHERE code = $1 and exist = True'

LOC_INFO_2_REQ = 'SELECT code, name, lvl, type, conqueror, cycle, status FROM loc WHERE name ILIKE $1 and exist = True'

LOC_INFO_GUILD_INFO = 'SELECT guild_tag, guild_emoji FROM loc_guilds WHERE code = $1'

LOC_MISS_REQ = 'SELECT code, name, lvl, type, conqueror, cycle, status FROM loc WHERE code LIKE $1 and exist = True'

LOC_BUFFS_REQ = 'SELECT code, name, lvl, type, conqueror, cycle, status FROM loc WHERE exist = True'

LOC_BUFFS_2_REQ = 'SELECT code, bless_json FROM loc_buff WHERE code = ANY($1::text[])'

LOC_OBJECTS_REQ = 'SELECT code, name, lvl, type, conqueror, cycle, status FROM loc WHERE type = $1 and exist = True'

LOC_MAP_BY_TIER_REQ = '''
SELECT code, name, lvl, type, conqueror, cycle, status FROM loc
WHERE conqueror = $1 and exist = True and $2 <= lvl and lvl <= $3 ORDER BY lvl
'''

LOC_MAP_BY_TYPE_REQ = '''
SELECT code, name, lvl, type, conqueror, cycle, status FROM loc
WHERE conqueror = $1 and type = $2 and exist = True ORDER BY lvl
'''

LOC_CHECK_SELECT_DELETED_REQ = '''
SELECT code, name, lvl, type, conqueror, cycle, status FROM loc WHERE code = ANY($1::text[]) ORDER BY lvl
'''

NEW_LOC_L_CHECK_FOR_TIER = '''
SELECT code, name, lvl, type, conqueror, cycle, status FROM loc WHERE $1 <= lvl and lvl < $2 and exist = True
'''

MARK_AS_DEAD_LOCATIONS = '''
UPDATE loc SET exist = False, death_time = LOCALTIMESTAMP WHERE code = ANY($1::text[])
'''

SETTINGS_GET_CHAT = '''
SELECT id, new_loc_ntf, delete_loc_ntf, brief_log, brief_mode, craft_ntf FROM chats WHERE id = $1
'''

NEW_LOC_NTF = '''
SELECT id, new_loc_ntf, delete_loc_ntf, brief_log, brief_mode, craft_ntf FROM chats WHERE new_loc_ntf = True
'''

DELETE_LOC_NTF = '''
SELECT id, new_loc_ntf, delete_loc_ntf, brief_log, brief_mode, craft_ntf FROM chats WHERE delete_loc_ntf = True
'''

ALLiANCE_UPDATE_MAIN = '''\
UPDATE alliance_hq
SET n_guilds = $1, n_members = $2, al_owner = $3, al_balance_pogs = $4, al_balance_money = $5, al_stock = $6,
al_glory = $7, al_main_raw = $8, al_main_last_update = LOCALTIMESTAMP WHERE al_code = $9
'''

ALLiANCE_UPDATE_ROSTER = '''
UPDATE alliance_hq
SET al_guilds = $1, al_roster_raw = $2, al_rost_last_update = LOCALTIMESTAMP WHERE al_code = $3
'''

WS_SHOPS_INSERT = '''
INSERT INTO ws_shops 
(link, name, ownertag, ownername, ownercastle, kind, mana, offers, castlediscount, guilddiscount, specialization,
qualitycraftlevel, specializations, maintenanceenabled, maintenancecost, date)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16)
ON CONFLICT (link) DO
UPDATE SET name = $2, ownertag = $3, ownername = $4, ownercastle = $5, kind = $6, mana = $7, offers = $8,
castlediscount = $9, guilddiscount = $10, specialization = $11, qualitycraftlevel = $12, specializations = $13,
maintenanceenabled = $14, maintenancecost = $15, date = $16
'''

STARTUP_GURU_SHOPS = '''
SELECT ws_shops.link, ws_shops.name, ws_shops.ownertag, ws_shops.ownername, ws_shops.ownercastle, ws_shops.mana,
ws_shops.offers, ws_shops.castlediscount, ws_shops.guilddiscount, ws_shops.specialization,
ws_shops.qualitycraftlevel, ws_shops.specializations, ws_shops.maintenanceenabled, ws_shops.maintenancecost,
ws_shops.date FROM ws_shops
INNER JOIN settings_date ON settings_date.var = 'ws_shops_upd'
WHERE ws_shops.date = settings_date.date
'''

GET_WS_LINK_SHOP = '''
SELECT link, name, ownertag, ownername, ownercastle, kind, mana, offers, castlediscount, guilddiscount, specialization,
qualitycraftlevel, specializations, maintenanceenabled, maintenancecost, date
FROM ws_shops WHERE link = $1
'''

BRIEF_GET_ALLIANCE_BY_GUILD_TAG = '''
SELECT loc.name, loc.code FROM loc
INNER JOIN loc_guilds on loc_guilds.code = loc.code
WHERE loc_guilds.guild_tag = $1
'''

BRIEF_INSERT_INTO_LOC_HISTORY_BREACH_AL = '''
INSERT INTO loc_history (code, date, url, txt) VALUES ($1, $2, $3, $4)
'''

BRIEF_NTF_REQ = '''
SELECT id, new_loc_ntf, delete_loc_ntf, brief_log, brief_mode, craft_ntf FROM chats WHERE brief_log = True
'''

BRIEF_GET_ALL_LOCS_REQ = '''
SELECT code, name, lvl, type, conqueror, cycle, status FROM loc WHERE type > 0 AND exist = True
'''

BRIEF_GET_GUILDS_BY_TAGS_REQ = '''
SELECT guild_tag, guild_emoji FROM loc_guilds WHERE guild_tag = any($1::text[])
'''

BRIEF_INSERT_GUILD_REQ = '''
INSERT INTO loc_guilds (code, guild_tag, guild_emoji) VALUES ($1, $2, $3)
ON CONFLICT (guild_tag) DO UPDATE SET code = $1, guild_emoji = $3
'''

BRIEF_GET_LOC_INFO_BY_NAME_REQ = '''
SELECT code, name, lvl, type, conqueror, cycle, status FROM loc WHERE name = $1 AND exist = True
'''