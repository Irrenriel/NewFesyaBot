MAIN_REQ = """
SELECT id, username, nickname, lvl, main_class, sub_class, guild_tag, castle, role, gm_role, hero_update FROM users;
"""

ADV_MAIN_REQ = "SELECT id, rank, reputation, avail_quests, inprog_quest, d_limit FROM adv_users;"

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