MAIN_REQ = '''
SELECT id, username, nickname, lvl, main_class, sub_class, guild_tag, castle, role, last_hero_update, gm_role FROM users
'''

ADV_MAIN_REQ = '''
SELECT id, rank, reputation, avail_quests, inprog_quest, d_limit FROM adv_users
'''