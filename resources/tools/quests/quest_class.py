import json
from datetime import datetime
from random import random
from typing import Union

import requests

from resources.models import db


class QuestsGenerator:
    """
    Players rank
    [0] - Max num of quest for rank
    [1] - Min and max num types of mobs
    [2] - Min and max num of mobs for type
    [3] - Available mode-types of tasks
    [4] - Min and max num of items for type to collect
    [5] - Min and max num of reward reputation

    {'packID' = 0,
     'packDate' = '01-01-2020'
     'packUserID' = 394557686,
     'packUserRank' = 1,
     'packQuests' = {
         1: {
             'questType': 'A',
             'questText': 'A far far away galaxy...',
             'questReward': 15
             'questTask': {
                 1: [1, "Wolf", "Forest", 2],
                 2: [1, "Boar", "Valley", 2]
                }
             },
         2: {
             'questType': 'F',
             'questText': 'See you in space, cowboy.',
             'questReward': 15
             'questTask': {
                 1: [1, "Sentinel", "Forbidden", 2]
                }
             },
         3: {
             'questType': 'F',
             'questText': 'Hello, world!',
             'questReward': 15
             'questTask': {
                1:  [1, "Blacksmith", "Forbidden", 3]
                }
             }
         }
     }
    """

    # rank : [0] max available quests, [1] num of tasks per quest, [2] num of kills per mob,
    # [3] available modes (1 - kill mobs, 2 - collect resources),
    _pRank = {1: [3, [1, 2], [2, 4], [1, 1], [0, 0], [5, 20]],
             2: [4, [1, 2], [2, 5], [1, 1], [0, 0], [15, 30]],
             3: [4, [1, 3], [2, 5], [1, 2], [1, 2], [25, 50]],
             4: [4, [2, 4], [3, 6], [1, 2], [2, 3], [30, 70]],
             5: [5, [3, 4], [4, 6], [1, 2], [2, 4], [50, 100]]
             }

    # Data of mob types
    _mob_types = {'A': ['Boar', 'Bear', 'Wolf'],
                 'F': ['Collector', 'Blacksmith', 'Alchemist', 'Knight', 'Ranger', 'Sentinel', 'Champion'],
                 'AnF': ['Boar', 'Bear', 'Wolf', 'Collector', 'Blacksmith',
                          'Alchemist', 'Knight', 'Ranger', 'Sentinel', 'Champion']}

    # Data of loot types
    _loot_types = {'A': ['Bone', 'Pelt'],
                  'F': ['Thread', 'Stick', 'Pelt', 'Bone', 'Coal', 'Charcoal', 'Powder'],
                  'AnF': ['Thread', 'Stick', 'Pelt', 'Bone', 'Coal', 'Charcoal', 'Powder']}

    # Data of animal types
    _animals_types = {'Wolf': ['Swamp', 'Forest', 'Valley'],
                     'Boar': ['Swamp', 'Forest', 'Valley'],
                     'Bear': ['Swamp', 'Forest', 'Valley']}

    # Little Cash for tasks
    _tasks_cash = []

    async def start(self, player_data: Union[tuple, list], db):
        self.resultQuests = {}
        self.player_rank = player_data[1]
        self.player_rank_data = self._pRank.get(self.player_rank)
        self.db = db

        # Create a dict`s 1-level info
        self.resultQuests['packID'] = await self._get_packID()
        self.resultQuests['packDate'] = datetime.now().strftime('%d-%m-%Y')
        self.resultQuests['packUserID'] = player_data[0]
        self.resultQuests['packUserRank'] = player_data[1]
        self.resultQuests['packQuests'] = await self._get_packQuests



    async def _get_packID(self):
        last_pack_id = await self.db.fetch('SELECT data_int FROM settings WHERE var = "q_pack_id"', one_row=True)
        pack_id = last_pack_id["dataint"] + 1
        self.db.execute('UPDATE settings SET data_int = data_int + 1 WHERE var = "q_pack_id"')
        return pack_id

    @property
    async def _get_packQuests(self):
        packQuests = {}

        # Get texts for quests from generator
        s = requests.Session()
        max_quests = self.player_rank_data[0]
        response = s.post('https://stormtower.ru/wp-content/themes/stormboot/gen/quest.php', data={'y': max_quests, 'z': 1})
        match_with_texts = []
        a = response.text.split("<div style='text-align:center;'>")
        for l in a[1:]:
            start_body = l.index('<p>')
            len_body = l.index('<img')
            match_with_texts.append(l[start_body+3:len_body].strip())
            for num in range(max_quests):
                packQuests[num + 1] = self._generate_quest(match_with_texts, num)
            return packQuests

            def _generate_quest(self, match_with_texts, num):
                dictQuest = {}

                # Choice a type of quest [A]nimals/[F]orbidden Clan
                questType = random.choice(['A', 'F'])
                dictQuest['questType'] = questType

                # Text of quest
                questText = match_with_texts[num]
                dictQuest['questText'] = questText

                # Reward of quest
                rr = self.player_rank_data[5]
                reward_rep = random.randint(rr[0], rr[1])
                dictQuest['questReward'] = reward_rep

                # Tasks of quest
                y = self.player_rank_data
                num_of_tasks = random.choice([y[1][0], y[1][1]])
                dictQuest['questTask'] = {}
                for i in range(num_of_tasks):
                    questTask = self._task_generator(questType)
                    dictQuest['questTask'][i + 1] = questTask
                    # print(i)

                return dictQuest

            def _task_generator(self, questsType):
                task = []

                # Mode Kill or Collect
                z = self.player_rank_data[3]
                mode = random.randint(z[0], z[1])
                task.append(mode)
                ttype, ttitle = None, None

                while ttype is None or f'{ttitle} {ttype}' in self._tasks_cash:
                    # Kill
                    if mode == 1:
                        ttype = random.choice(self._mob_types.get(questsType))
                        task.append(ttype)

                        ttitle = random.choice(self._animals_types.get(ttype, ['Forbidden']))
                        task.append(ttitle)

                        t = self.player_rank_data[2]
                        tnum = random.randint(t[0], t[1]) if ttype != 'Champion' else 1
                        task.append(tnum)


                    # Collect
                    elif mode == 2:
                        ttype = random.choice(self._loot_types.get(questsType))
                        task.append(ttype)

                        ttitle = '*'
                        task.append(ttitle)

                        t = self.player_rank_data[4]
                        tnum = random.randint(t[0], t[1])
                        task.append(tnum)

                    else:
                        raise Exception('Impossible Else')
                else:
                    self._tasks_cash.append(f'{ttitle} {ttype}')

                return task

    def get_pack(self):
        # return self.resultQuests
        return self.resultQuests.get('packID'), json.dumps(self.resultQuests)