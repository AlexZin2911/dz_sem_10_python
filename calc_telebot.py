import telebot
from telebot import types
from datetime import datetime as dt
import logger

bot = telebot.TeleBot('TOKEN')

value = ''
old_value = ''

keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.row(telebot.types.InlineKeyboardButton(' ', callback_data='no'),
             telebot.types.InlineKeyboardButton('C', callback_data='C'),
             telebot.types.InlineKeyboardButton('<=', callback_data='<='),
             telebot.types.InlineKeyboardButton('/', callback_data='/'))
keyboard.row(telebot.types.InlineKeyboardButton('7', callback_data='7'),
             telebot.types.InlineKeyboardButton('8', callback_data='8'),
             telebot.types.InlineKeyboardButton('9', callback_data='9'),
             telebot.types.InlineKeyboardButton('*', callback_data='*'))
keyboard.row(telebot.types.InlineKeyboardButton('4', callback_data='4'),
             telebot.types.InlineKeyboardButton('5', callback_data='5'),
             telebot.types.InlineKeyboardButton('6', callback_data='6'),
             telebot.types.InlineKeyboardButton('-', callback_data='-'))
keyboard.row(telebot.types.InlineKeyboardButton('1', callback_data='1'),
             telebot.types.InlineKeyboardButton('2', callback_data='2'),
             telebot.types.InlineKeyboardButton('3', callback_data='3'),
             telebot.types.InlineKeyboardButton('+', callback_data='+'))
keyboard.row(telebot.types.InlineKeyboardButton(' ', callback_data='no'),
             telebot.types.InlineKeyboardButton('0', callback_data='0'),
             telebot.types.InlineKeyboardButton(',', callback_data='.'),
             telebot.types.InlineKeyboardButton('=', callback_data='='))


@bot.message_handler(commands=['start'])
def getMessage(message):
    global value
    if value == '':
        bot.send_message(message.from_user.id,
                         '0', reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id,
                         value, reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def getMessage1(message):
    global value
    bot.send_message(message.from_user.id, '<b><u>Справка:</u></b>\n', parse_mode='html')
    bot.send_message(message.from_user.id,f'Используются стандартные операторы для подсчета\n'
                                        '"-" - вычитание\n"+" - сложение\n"*" - умножение\n'
                                        '"/" - деление\n"С" - очистить поле\n"<=" - стереть 1 символ\n'
                                        '"," - запятая(для дробей)\n"**" - возведение в степень\n"=" - равно\n'
                                        'обыкновенные дроби записываются через "/" (Пример: числитель/знаменатель)'
                                        'Логгирование происходит в файл "log.txt", который находится в корневой папке проекта.')


@bot.callback_query_handler(func=lambda call: True)
def callback_func(query):
    global value, old_value
    data = query.data
    if data == 'no':
        pass
    elif data == 'C':
        value = ''
    elif data == '<=':
        if value != '':
            value = value[:len(value)-1]
    elif data == '=':
        value = str(eval(value))
    else:
        value += data
    if value != old_value:
        if value == '':
            bot.edit_message_text(
                chat_id=query.message.chat.id, message_id=query.message.id, text='0', reply_markup=keyboard)
        else:
            bot.edit_message_text(chat_id=query.message.chat.id,
                                  message_id=query.message.id, text=value, reply_markup=keyboard)
        old_value = value

    logger.logger(f'{value}')

bot.polling()
