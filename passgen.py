import telebot
from telebot import types
from string import digits
from random import choice
import pymssql

con = pymssql.connect(host='den1.mssql3.gear.host',user='testbuddrugom',password='Halabuda_2017',database='testbuddrugom')
cursor = con.cursor()

TOKEN = '509247585:AAFpJ_Q2eOsn_vt7L5XWrN4beKrKfVrv9JA'
bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start'])

def start(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_phone, button_geo)
    musor = bot.send_message(message.chat.id, text='musora',  reply_markup=keyboard)
    # bot.send_message(message.chat.id, message.text)
    # print(message.text)
    # print('asdfasdf')
    bot.register_next_step_handler(musor, checkphone)

@bot.message_handler(commands=['sendphone'])
def checkphone(message):
    phone = bot.send_message(message.chat.id,message.contact.phone_number[2:])
    cursor.execute("declare @check int set @check= 0 SELECT  @check = case when Count(mobile_number) is not null then 1 "
                   "else 0 end  FROM users WHERE mobile_number = {phone_number} group by(mobile_number) select @check as"
                   " result".format(phone_number=message.contact.phone_number[2:]))
    result = cursor.fetchone()
    check, = result
    check = int(check)
    if check == 1:
        bot.register_next_step_handler(phone, signin)
        signin(message)
    else:
        bot.send_message(message.chat.id, "Войдите в телеграм с учетной записи, номер которой зарегистрирован в приложении")

@bot.message_handler(commands=['signin'])
def signin(message):
    password = ""
    bot.send_message(message.chat.id, 'Ваш пароль для входа в приложение:{password}'.format(password = password.join([choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ' + digits) for i in range(6)])))

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

