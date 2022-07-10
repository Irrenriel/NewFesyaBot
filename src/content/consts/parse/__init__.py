HERO_PARSE = r'(?P<castle>[☘️🖤🦇🌹🍁🐢🍆])(?:(?!\[)(?P<guilds_emoji>\W)|)(?:(?=\[)\[(?P<guild_tag>.+)\]|)(?P<nickname>.+)\n' \
             r'🏅Уровень: (?P<lvl>\d+).*\n.*\n.*\n.*\n.*\n(?:(?=💧).*\n|).*\n.*\n.*\n' \
             r'(?P<class>[🏛⚔️🏹⚗️🐣🛡🩸⚒📦🎩]+)'

AL_MAIN_PARSE = r'🤝(?P<al_name>.+)\s\nGuilds:\s(?P<n_guilds>\d+)\s👥(?P<n_members>\d+)\n' \
                r'Owner:.*\[(?P<al_owner>\w+)\].+\n.+\n.+\nBalance:\n\s+(👝(?P<al_balance_pogs>\d+))?(\s+)?💰(?P<al_balance_money>\d+)(.+)?\n' \
                r'(\s+)?📦Stock:\s(?P<al_stock>\d+)\n\s+(\s+)?🎖Glory:\s(?P<al_glory>\d+)'

NEW_LOC_INPUT_PARSE = r'(?=You found hidden location)(?:You found hidden location (?P<loc_name>.*)) lvl.(?P<loc_lvl>\d+)\n' \
                      r'((?=То remember)|.+\n).+ (?P<loc_code>.+)|(?:You found hidden headquarter (?P<head_name>.*))\n' \
                      r'.+: (?P<head_code>.+)$'

BRIEF_ALLIANCE_PARSE = r'(?P<name>.+) was (?P<status>.+)(?:\:|\. )\n' \
                       r'(?:(?=Attackers).+ (?P<stock>\d+|)📦 and (?P<glory>\d+|)🎖|)'

BRIEF_LOCATIONS_PARSE = r'(?P<name>.+) lvl\.(?P<lvl>\d+) (?:(?=was)was (?P<def_status>.+)|belongs to ((?P<new_conqueror>\w+.\w+)(?P<atk_status>.+)\n)?)'
