HERO_PARSE = r'(?P<castle>[☘️🖤🦇🌹🍁🐢🍆])(?:(?!\[)(?P<guilds_emoji>\W)|)(?:(?=\[)\[(?P<guild_tag>.+)\]|)(?P<nickname>.+)\n' \
             r'🏅Уровень: (?P<lvl>\d+).*\n.*\n.*\n.*\n.*\n(?:(?=💧).*\n|).*\n.*\n.*\n' \
             r'(?P<class>[🏛⚔️🏹⚗️🐣🛡🩸⚒📦🎩]+)'

AL_MAIN_PARSE = r'🤝(?P<al_name>.+)\s\nGuilds:\s(?P<num_guilds>\d+)\s👥(?P<num_people>\d+)\n' \
                r'Owner:.*\[(?P<al_leader>\w+)\].+\n.+\n.+\nBalance:\n\s+(👝(?P<b_pogs>\d+))?(\s+)?💰(?P<b_money>\d+)(.+)?\n' \
                r'(\s+)?📦Stock:\s(?P<stock>\d+)\n\s+(\s+)?🎖Glory:\s(?P<glory>\d+)'

NEW_LOC_INPUT_PARSE = r'(?=You found hidden location)(?:You found hidden location (?P<loc_name>.*)) lvl.(?P<loc_lvl>\d+)\n' \
                      r'((?=То remember)|.+\n).+ (?P<loc_code>.+)|(?:You found hidden headquarter (?P<head_name>.*))\n' \
                      r'.+: (?P<head_code>.+)$'
