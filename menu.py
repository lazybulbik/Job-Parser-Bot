from telebot.types import *
from parser import city_id, cities

# Main menu
start_parsing = InlineKeyboardButton('Начать парсинг', callback_data='start_parsing')
change_delay = InlineKeyboardButton('Заменить частоту парсинга', callback_data='change_delay')
add_place = InlineKeyboardButton('Редактировать города', callback_data='redact_place')

main_menu = InlineKeyboardMarkup(row_width=1).add(start_parsing, change_delay, add_place)


def get_cities_button():
    menu = InlineKeyboardMarkup(row_width=3)

    btns = []
    for city in city_id:
        if city in cities:
            button = InlineKeyboardButton(f'🌟{city_id[city]}', callback_data=f'remove_city:{city}')
        else:
            button = InlineKeyboardButton(f'{city_id[city]}', callback_data=f'set_city:{city}')

        btns.append(button)

    back = InlineKeyboardButton('Назад', callback_data='back')
    menu.add(*btns)
    menu.add(back)

    return menu