MAIN_REQ = '''
SELECT id, username, nickname, lvl, main_class, sub_class, guild_tag, castle, role, last_hero_update, gm_role FROM users
'''

ADV_MAIN_REQ = '''
SELECT id, rank, reputation, avail_quests, inprog_quest, d_limit FROM adv_users
'''

ACTIVE_LOG_REQ_BY_USER = '''
SELECT id, username, info, time, date FROM active_log WHERE username = $1 ORDER BY time DESC
'''

ACTIVE_LOG_REQ_BY_NONE = '''
SELECT id, username, info, time, date FROM active_log ORDER BY time DESC
'''

J_LOGGING_REQ = f'''
INSERT INTO $1 VALUES (?,?,?, strftime('%s','now', 'localtime'), datetime('now', 'localtime'))
'''