import telebot
from telebot import types
from string import digits
from random import choice
import pymssql

con = pymssql.connect(host='den1.mssql3.gear.host',user='testbuddrugom'
                      ,password='Halabuda_2017',database='testbuddrugom')
cursor = con.cursor()

TOKEN = '509247585:AAFpJ_Q2eOsn_vt7L5XWrN4beKrKfVrv9JA'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard = True)
    button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
    keyboard.add(button_phone)
    prev_message = bot.send_message(message.chat.id, text='Отправьте нам Ваши контакты, чтобы мы могли быстро и легко '
                                                          'зарегистрировать Вас в приложении!',  reply_markup=keyboard)
    bot.register_next_step_handler(prev_message, signup)
# def checkphone(message):
#     phone = bot.send_message(message.chat.id,"Номер проверен на наличие в нашей базе данных")
#     cursor.execute("declare @check int set @check= 0 SELECT  @check = case when Count(mobile_number) is not null then 1 "
#                    "else 0 end  FROM users WHERE mobile_number = {phone_number} group by(mobile_number) select @check as"
#                    " result".format(phone_number=message.contact.phone_number[2:]))
#     result = cursor.fetchone()
#     check, = result
#     check = int(check)
#     if check == 1:
#         bot.register_next_step_handler(phone, signup)
#         signup(message)
#     else:
#         bot.send_message(message.chat.id, "Данный номер не зарегистрирован")

@bot.message_handler(commands=['signup'])
def signup(message):
    try:
        password = ""
        random_password = password.join([choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ' + digits) for i in range(6)])
        if message.from_user.id == message.contact.user_id:
            cursor.execute("exec insertIntoUserTable @phoneNumber = '{phone_number}', @code = '{password}', @user_name = "
                           "'{username}'".format(username = message.chat.username, password = random_password,
                            phone_number = message.contact.phone_number[2:]))
            con.commit()
            bot.send_message(message.chat.id, "{random_password}".format(random_password=random_password))
            bot.send_message(message.chat.id, "Добро пожаловать, для входа в приложение используйте вышеуказанный код")
        else:
            bot.send_message(message.chat.id, "Похвально, что Вы хотите зарегистрировать друга, но мы уверены что он "
                                              "уже взрослый и может сам справится нажатием трех клавиш.")
            start(message)
    except AttributeError:
        bot.send_message(message.chat.id, "Прошу прощения, но это явно не похоже на Ваши контакты, попробуйте еще")
        start(message)



bot.polling(none_stop=True)

