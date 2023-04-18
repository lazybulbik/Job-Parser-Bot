import telebot
import os
from config.config import TOKEN
import menu
import parser
# import proxy

bot = telebot.TeleBot(TOKEN)

admin_id = None


@bot.message_handler(commands=['start'])
def start_using(message: telebot.types.Message):
    global admin_id
    dir = os.listdir('config/')

    if 'chanel_id.txt' not in dir:
        bot.send_message(message.from_user.id, 'После первого запуска необходимо настроить бота. '
                                               '\n\nДобавьте бота в канал, в который необходимо публиковать посты.'
                                               'После отправьте в канал команду /start')

        admin_id = message.from_user.id

    else:
        bot.send_message(message.from_user.id, 'Вы в главном меню', reply_markup=menu.main_menu)


@bot.channel_post_handler(commands=['start'])
def get_first_launch(message: telebot.types.Message):
    with open('config/chanel_id.txt', 'w') as file:
        file.write(str(message.chat.id))

    bot.send_message(admin_id, f'Отлично! Теперь я буду отправлять новые вакансии в канал *{message.chat.title}*')
    bot.send_message(admin_id, 'Вы в главном меню', reply_markup=menu.main_menu)


@bot.callback_query_handler(func=lambda call: True)
def call_back(callback_query: telebot.types.CallbackQuery):
    if callback_query.data == 'back':
        bot.edit_message_text('Вы в главном меню',
                              message_id=callback_query.message.message_id,
                              chat_id=callback_query.from_user.id,
                              reply_markup=menu.main_menu)

    if callback_query.data == 'start_parsing':
        if parser.pause:
            if len(parser.cities) != 0:
                parser.pause = False

                menu.start_parsing.text = 'Завершить парсинг'
                bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id,
                                              reply_markup=menu.main_menu)
            else:
                bot.send_message(callback_query.from_user.id, 'Вы не выбрали города для парсинга')
        else:
            parser.pause = True

            menu.start_parsing.text = 'Начать парсинг'
            bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id,
                                          reply_markup=menu.main_menu)

    if callback_query.data == 'change_delay':
        def change_delay(message: telebot.types.Message):
            try:
                delay = int(message.text)
                parser.delay = delay
            except:
                bot.send_message(callback_query.from_user.id, 'Введите целое число!')
            finally:
                bot.send_message(callback_query.from_user.id, 'Вы в главном меню', reply_markup=menu.main_menu)

        bot.edit_message_text('Ведите время через которое проверять наличие вакансий. (В часах)',
                              message_id=callback_query.message.message_id,
                              chat_id=callback_query.from_user.id)
        bot.register_next_step_handler(callback_query.message, change_delay)

    if callback_query.data == 'redact_place':
        bot.edit_message_text('Выбор мест',
                              message_id=callback_query.message.message_id,
                              chat_id=callback_query.from_user.id,
                              reply_markup=menu.get_cities_button())

    if 'set_city' in callback_query.data:
        parser.cities.append(int(callback_query.data.split(':')[1]))
        parser.last_idies[int(callback_query.data.split(':')[1])] = ''

        bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      reply_markup=menu.get_cities_button())

    if 'remove_city' in callback_query.data:
        parser.cities.remove(int(callback_query.data.split(':')[1]))
        del parser.last_idies[int(callback_query.data.split(':')[1])]

        bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                      message_id=callback_query.message.message_id,
                                      reply_markup=menu.get_cities_button())

print('start')

while True:
    try:
      bot.polling(none_stop=True, timeout=25)
    except Exception as e:
      print(e)