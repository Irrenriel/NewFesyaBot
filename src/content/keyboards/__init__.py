from config import config
from resources.tools.keyboards import ReplyKeyboard, InlineKeyboard, Call

from src.content import UserData


# /start
def start_kb(user: UserData):
    keys = ['🗳Меню', '🎪Альянс']

    # Append для Таверны!
    # ...

    if user.guild_tag == 'AT':
        keys.append('⚖️Биржа')

    if user.id in config.WORKBENCH_MEMBERS_IDS:
        keys.append('⚒Мастерская')

    return ReplyKeyboard(*keys)


def donate_kb():
    return InlineKeyboard(
        Call('🔄Обновить', 'updDonate'), Call('❌Отменить', 'declDonate'), Call('💰Оплатить', 'doneDonate'), row_width=2
    )


def adv_guild_kb():
    return ReplyKeyboard('📋Статус', '📜Квесты', 'Вернуться↩', row_width=2)