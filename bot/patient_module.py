import telebot
bot = telebot.TeleBot('1821024057:AAHb2eXSxUNQx7adl2XML-iSiVOC0AFK9OM')
from telebot import types
from update_module import *

bot.message_handler(content_types=['text'])
def patient_bot(message, user_login):
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Просмотреть свои данные")
    button2 = types.KeyboardButton("Выйти")
    markup1.add(button1, button2)
    bot.send_message(message.chat.id, "Добро пожаловать!", reply_markup=markup1)
    bot.register_next_step_handler(message, show_my_data_id(user_login))
    #bot.send_message(message.from_user.id, show_my_data_id(user_login))

def show_my_data_id(user_login):
    output = ''
    temp_data = ''
    dic = update_data()
    number = dic['Логин'].index(user_login)
    for i in dic:
        if i == 'ID' or i == 'Логин' or i == 'Пароль' or i == 'Ссылка на фото':
            pass
        elif dic[i][number] == None:
            output = i + ': ' + 'информация отсутствует'
            temp_data += output + '\n'
        else:
            output = i + ': ' + str(dic[i][number])
            temp_data += output + '\n'

    analis = update_analysis()
    temp_data += 'Анализы:\n'
    flag = 0
    for i in analis:
        if i[-1] == id:
            temp_data += i[1] + ': ' + i[2] + '\n'
            flag = 1
    if flag == 0:
        temp_data += 'Отсутствуют'
    return temp_data
