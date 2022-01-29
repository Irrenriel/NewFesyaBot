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

AL_GET_GUILD_REQ = '''
SELECT al_name, alliance_hq.al_code, al_owner, users.username, alliance_hq.n_members, n_guilds, al_guilds
FROM alliance_guilds
INNER JOIN alliance_hq ON alliance_guilds.al_code = alliance_hq.al_code
INNER JOIN users ON alliance_hq.al_leader = users.id
WHERE alliance_guilds.guild_tag = $1
'''

REG_NEW_ALLIANCE = '''
INSERT INTO alliance_hq (
    al_code, al_name, al_owner, al_leader, n_members, n_guilds, al_balance_pogs,
    al_balance_money, al_stock, al_glory, al_guilds, al_main_raw, al_roster_raw,
    al_main_last_update, al_rost_last_update
)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $10, $11, $12, LOCALTIMESTAMP, LOCALTIMESTAMP)
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
SELECT code, name, lvl, type, conqueror, cycle, status FROM loc WHERE $1 <= lvl and lvl < $2
'''

MARK_AS_DEAD_LOCATIONS = '''
UPDATE loc SET exist = False, death_time = LOCALTIMESTAMP WHERE code = ANY($1::text[])
'''

SETTINGS_GET_CHAT = '''
SELECT id, new_loc_ntf, delete_loc_ntf, brief_log, brief_mode, craft_ntf FROM chats WHERE id = $1
'''
