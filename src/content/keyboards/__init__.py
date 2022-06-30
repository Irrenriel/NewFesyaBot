from resources.tools.keyboards import ReplyKeyboard, InlineKeyboard, Call


# /start
def start_kb():
    return ReplyKeyboard('🗳Меню', '🎪Альянс')

def donate_kb():
    return InlineKeyboard(
        Call('🔄Обновить', 'updDonate'), Call('❌Отменить', 'declDonate'), Call('💰Оплатить', 'doneDonate'), row_width=2
    )