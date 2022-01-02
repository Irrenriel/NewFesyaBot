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