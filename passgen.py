import telebot
import sqlite3
from string import digits
from random import choice

TOKEN = '509247585:AAFpJ_Q2eOsn_vt7L5XWrN4beKrKfVrv9JA'
bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, уважаемый пользователь приложение Будь Другом, '
                                             'для того чтобы зарегистрироваться в системе введи /signup,'
                                             'если же ты хочешь получить код для входа в систему следует ввести /signin')


@bot.message_handler(commands=['signin'])
def signin(message):
    password = ""
    bot.send_message(message.chat.id, 'Твой пароль для входа в приложение:{password}'.format(name=message.text,password = password.join([choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ' + digits) for i in range(6)]) ))

@bot.message_handler(commands=['signup'])
def signup(message):
    name = bot.send_message(message.chat.id, 'Введите свое имя')
    bot.register_next_step_handler(name, faculty)

def faculty(message):
    if any(map(str.isdigit, message.text)) == True:
        bot.send_message(message.chat.id, 'Ваше имя содержит недопустимые символы, /signup')
    else:
        faculty_name = bot.send_message(message.chat.id, 'Введите название факультета')
        bot.register_next_step_handler(faculty_name, hostel)

def hostel(message):
    hostel_number = bot.send_message(message.chat.id, 'Введите номер общежития(не обязательно)')
    bot.register_next_step_handler(hostel_number, last_check)

def last_check(message):
    if any(map(str.isalpha, message.text)) == True:
        bot.send_message(message.chat.id, 'Номер общежития содержит буквы, /signup')
    else:
        bot.send_message(message.chat.id, 'Спасибо за регистрацию!')

bot.polling(none_stop=True)
