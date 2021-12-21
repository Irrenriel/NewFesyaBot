HERO_PARSE = r'(?P<castle>[☘️🖤🦇🌹🍁🐢🍆])(?:(?!\[)(?P<guilds_emoji>\W)|)(?:(?=\[)\[(?P<guild_tag>.+)\]|)(?P<nickname>.+)\n' \
             r'🏅Уровень: (?P<lvl>\d+).*\n.*\n.*\n.*\n.*\n(?:(?=💧).*\n|).*\n.*\n.*\n' \
             r'(?P<class>[⚒📦⚗️⚔️🛡🏹🏛🩸🎩])(?:(?=Класс)|(?P<sub_class>[⚒📦⚗️⚔️🛡🏹🩸🎩]))'
