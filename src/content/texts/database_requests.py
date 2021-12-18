MAIN_REQ = '''
SELECT id, username, nickname, lvl, main_class, sub_class, guild_tag, castle, role, last_hero_update, gm_role FROM users
'''

ADV_MAIN_REQ = '''
SELECT id, rank, reputation, avail_quests, inprog_quest, d_limit FROM adv_users
'''

ACTIVITY_LOGGING_REQ_BY_USER = '''
SELECT id, username, data, time, date FROM activity_logger_fesya WHERE username = $1 ORDER BY date DESC
'''

ACTIVITY_LOGGING_REQ_BY_NONE = '''
SELECT id, username, data, time, date FROM activity_logger_fesya ORDER BY date DESC
'''

ACTIVITY_LOGGING_REQ_INSERT = f'''
INSERT INTO activity_logger_fesya (id, username, data) VALUES ($1, $2, $3)
'''