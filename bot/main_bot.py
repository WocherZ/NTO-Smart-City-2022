import telebot
from telebot import types
#import sql_module
import sqlite3
from update_module import *
from sql_auth_module import *
from patient_module import *

bot = telebot.TeleBot('1821024057:AAHb2eXSxUNQx7adl2XML-iSiVOC0AFK9OM')

from sql_module import read_sqlite_table

logs_doct = sql_auth_doct(records=[])
logs_pat = sql_auth_pat(records=[])
if_doct = True

new_patient = {
    'ID': None,
    'Имя': None,
    'Фамилия': None,
    'Логин': None,
    'Пароль': None,
    'Возраст': None,
    'Рост': None,
    'Вес': None,
    'Лечащий доктор': None,
    'Комната': None,
    'Ссылка на фото': None,
    'Диагноз': None,
    'Пол': None
    }

dic = update_data()

patients = []

@bot.message_handler(commands=["start"])
def auth(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Я врач")
    button2 = types.KeyboardButton("Я пациент")
    markup.add(button1, button2)
    bot.send_message(message.chat.id, "Выберите нужное окно", reply_markup=markup)

@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Просмотреть данные")
    button2 = types.KeyboardButton("Изменить данные пациента")
    button3 = types.KeyboardButton("Ввести нового пациента")
    button4 = types.KeyboardButton("Удалить пациента из базы")
    markup.add(button1, button2, button3, button4)
    bot.send_message(message.chat.id, "Главное меню:", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global new_patient
    global new_add_patient
    no_butt = types.ReplyKeyboardRemove()

    if message.text == "Просмотреть данные" or message.text == "Другой пациент":
        bot.send_message(message.from_user.id, 'Введите ID пациента', reply_markup=no_butt)
        bot.register_next_step_handler(message, watch_data)

    elif message.text == "Удалить пациента из базы":
        bot.send_message(message.from_user.id, "Введите ID пациента, которого надо удалить из базы")
        bot.register_next_step_handler(message, delete_pat)

    elif message.text == "Я врач":
        global if_doct
        if_doct = True
        bot.send_message(message.from_user.id, 'Введите логин', reply_markup=no_butt)
        bot.register_next_step_handler(message, auth_login)
    elif message.text == "Я пациент":
        if_doct = False
        bot.send_message(message.from_user.id, 'Введите логин', reply_markup=no_butt)
        bot.register_next_step_handler(message, auth_login)
    elif message.text == 'Просмотреть свои данные':
        bot.send_message(message.from_user.id, show_my_data_id(user_login))
    elif message.text == 'Выйти':
        auth(message)

    elif message.text == 'aaa':
        print(dic)

    elif message.text == "Изменить данные пациента":
        bot.send_message(message.from_user.id, 'Введите ID пациента', reply_markup=no_butt)
        bot.register_next_step_handler(message, get_data)

    elif message.text == 'Ввести нового пациента':
        bot.send_message(message.from_user.id, 'Придумайте логин', reply_markup=no_butt)
        bot.register_next_step_handler(message, get_login)

    elif message.text == 'Имя':
        bot.send_message(message.from_user.id, 'Введите имя пациента', reply_markup=no_butt)
        bot.register_next_step_handler(message, get_name)
    elif message.text == 'Фамилия':
        bot.send_message(message.from_user.id, 'Введите фамилию пациента', reply_markup=no_butt)
        bot.register_next_step_handler(message, get_surname)
    elif message.text == 'Пол':
        bot.send_message(message.from_user.id, 'Введите пол пациента', reply_markup=no_butt)
        bot.register_next_step_handler(message, get_gender)
    elif message.text == 'Возраст':
        bot.send_message(message.from_user.id, 'Введите возраст пациента', reply_markup=no_butt)
        bot.register_next_step_handler(message, get_age)
    elif message.text == 'Вес':
        bot.send_message(message.from_user.id, 'Введите вес пациента', reply_markup=no_butt)
        bot.register_next_step_handler(message, get_weight)
    elif message.text == 'Рост':
        bot.send_message(message.from_user.id, 'Введите рост пациента', reply_markup=no_butt)
        bot.register_next_step_handler(message, get_hight)

    elif message.text == 'Добавить рост':
        bot.send_message(message.from_user.id, 'Введите рост пациента', reply_markup=no_butt)
        bot.register_next_step_handler(message, get_hight2)
    elif message.text == 'Добавить вес':
        bot.send_message(message.from_user.id, 'Введите вес пациента', reply_markup=no_butt)
        bot.register_next_step_handler(message, get_weight2)
    elif message.text == 'Добавить возраст':
        bot.send_message(message.from_user.id, 'Введите возраст пациента', reply_markup=no_butt)
        bot.register_next_step_handler(message, get_age2)

    elif message.text == 'Главное меню':
        start(message)
        if new_patient['ID'] != None:
            patients.append(new_patient)
            new_patient = {
                'ID': None,
                'Имя': None,
                'Фамилия': None,
                'Логин': None,
                'Пароль': None,
                'Возраст': None,
                'Рост': None,
                'Вес': None,
                'Лечащий доктор': None,
                'Комната': None,
                'Ссылка на фото': None,
                'Диагноз': None,
                'Пол': None
                }

        into_sql(patients)
    elif message.text == 'Сохранить':
        start(message)
        add_sql_patient(new_add_patient)
        new_add_patient = {
            'ID': None,
            'Имя': None,
            'Фамилия': None,
            'Логин': None,
            'Пароль': None,
            'Возраст': None,
            'Рост': None,
            'Вес': None,
            'Лечащий доктор': None,
            'Комната': None,
            'Ссылка на фото': None,
            'Диагноз': None,
            'Пол': None
            }

def watch_data(message):
    id = message.text
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['Другой пациент', 'Главное меню']
    menu.add(*buttons)
    try:
        bot.send_message(message.from_user.id, show_data_id(int(id)), reply_markup=menu)
    except ValueError:
        bot.send_message(message.from_user.id, text="Введите ID пациента в виде целового числа")
        bot.register_next_step_handler(message, watch_data)

user_login = ''
def auth_login(message):
    global user_login
    user_login = message.text
    no_butt = types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, 'Введите пароль', reply_markup=no_butt)
    bot.register_next_step_handler(message, auth_pass)

def auth_pass(message):
    global user_login
    global if_doct
    user_pass = message.text
    if if_doct:
        identify(user_login, user_pass, message)
    else:
        ident_pat(user_login, user_pass, message)

def identify(user_login, user_pass, message):
    for i in logs_doct:
        if i == (user_login, user_pass):
            start(message)
            return
    bot.send_message(message.from_user.id, 'Неправильный логин или пароль. Попробуйте ещё раз')
    bot.send_message(message.from_user.id, 'Введите логин')
    bot.register_next_step_handler(message, auth_login)

def ident_pat(user_login, user_pass, message):
    for i in logs_pat:
        if i == (user_login, user_pass):
            patient_bot(message, user_login)
            return

    bot.send_message(message.from_user.id, 'Неправильный логин или пароль. Попробуйте ещё раз')
    bot.send_message(message.from_user.id, 'Введите логин')
    bot.register_next_step_handler(message, auth_login)

def show_data_id(id):
    output = ''
    temp_data = ''
    try:
        number = dic['ID'].index(id)
    except ValueError:
        return 'Такого пациента нет в базе данных'
    for i in dic:
        if i == 'ID' or i == 'Логин' or i == 'Пароль' or i == 'Ссылка на фото':
            pass
        elif  dic[i][number] == None:
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

@bot.message_handler(content_types='text')
def get_data(message):
    global new_patient
    patients_id = message.text
    try:
        new_patient['ID'] = int(patients_id)
        button(message)
    except ValueError:
        bot.send_message(message.from_user.id, text='Введите ID в виде целового числа')
        bot.register_next_step_handler(message, get_data)

def button(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['Имя', 'Фамилия', 'Пол', 'Возраст', 'Вес', 'Рост', 'Главное меню']
    keyboard.add(*buttons)
    bot.send_message(message.from_user.id, 'Выберите параметр, который хотите ввести', reply_markup=keyboard)

def get_name(message):
    global new_patient
    name = message.text
    new_patient['Имя'] = name
    button(message)

def get_surname(message):
    global new_patient
    surname = message.text
    new_patient['Фамилия'] = surname
    button(message)

def get_gender(message):
    global new_patient
    gender = message.text
    new_patient['Пол'] = gender
    button(message)

def get_age(message):
    global new_patient
    age = message.text
    try:
        new_patient['Возраст'] = int(age)
        button(message)
    except ValueError:
        bot.send_message(message.from_user.id, text='Введите возраст в виде целого числа')
        bot.register_next_step_handler(message, get_age)

def get_weight(message):
    global new_patient
    weight = message.text
    try:
        new_patient['Вес'] = float(weight)
        button(message)
    except ValueError:
        bot.send_message(message.from_user.id, 'Введите вес в виде числа')
        bot.register_next_step_handler(message, get_weight)

def get_hight(message):
    global new_patient
    height = message.text
    try:
        new_patient['Рост'] = float(height)
        button(message)
    except ValueError:
        bot.send_message(message.from_user.id, text='Введите рост в виде числа')
        bot.register_next_step_handler(message, get_hight)

def into_sql(patients):
    global dic

    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()

    eng_dict = {
        'ID': 'id',
        'Имя': 'first_name',
        'Фамилия': 'last_name',
        'Пол': 'gender',
        'Возраст': 'age',
        'Вес': 'weight',
        'Рост': 'height',
        'Комната': 'room_id',
        'Лечащий доктор': 'doctor_id',
        'Ссылка на фото': 'image_link',
        'Диагноз': 'diagnosis'
    }

    for i in patients:
        for field in i.items():
            #print(eng_dict[field[0]], field[1], list(i.values())[0])
            if field[1] != None:
                if type(field[1]) == str:
                    cursor.execute(f"""UPDATE app_patient set {eng_dict[field[0]]} = '{field[1]}' WHERE id = {list(i.values())[0]}""")
                    connection.commit()
                else:
                    cursor.execute(f"""UPDATE app_patient set {eng_dict[field[0]]} = {field[1]} WHERE id = {list(i.values())[0]}""")
                    connection.commit()
                # else:
                #     cursor.execute(f"""UPDATE app_patient set {eng_dict[field[0]]} = null WHERE id = {list(i.values())[0]}""")
                #     connection.commit()

    connection.close()
    dic = update_data()

new_add_patient = {
    'ID': None,
    'Имя': None,
    'Фамилия': None,
    'Логин': None,
    'Пароль': None,
    'Возраст': None,
    'Рост': None,
    'Вес': None,
    'Лечащий доктор': None,
    'Комната': None,
    'Ссылка на фото': None,
    'Диагноз': None,
    'Пол': None
    }

def get_login(message):
    global new_add_patient
    login = message.text
    new_add_patient['Логин'] = login
    bot.send_message(message.from_user.id, 'Придумайте пароль')
    bot.register_next_step_handler(message, get_passw)

def get_passw(message):
    global new_add_patient
    passw = message.text
    new_add_patient['Пароль'] = passw
    bot.send_message(message.from_user.id, 'Введите имя пациента')
    bot.register_next_step_handler(message, get_f_name)

def get_f_name(message):
    global new_add_patient
    first_name = message.text
    new_add_patient['Имя'] = first_name
    bot.send_message(message.from_user.id, 'Введите фамилию пациента')
    bot.register_next_step_handler(message, get_l_name)

def get_l_name(message):
    global new_add_patient
    last_name = message.text
    new_add_patient['Фамилия'] = last_name
    bot.send_message(message.from_user.id, 'Введите пол пациента')
    bot.register_next_step_handler(message, get_gender2)

def get_gender2(message):
    global new_add_patient
    gender = message.text
    if gender == 'М' or gender == 'Ж':
        new_add_patient['Пол'] = gender
        button2(message)
    else:
        bot.send_message(message.from_user.id, 'Введите одну букву: М - мужской пол, Ж - женский пол')
        bot.register_next_step_handler(message, get_gender2)


def button2(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['Добавить возраст', 'Добавить вес', 'Добавить рост', 'Сохранить']
    keyboard.add(*buttons)
    bot.send_message(message.from_user.id, 'Можете ввести дополнительную информацию', reply_markup=keyboard)

def get_hight2(message):
    global new_add_patient
    hight = message.text
    try:
        new_add_patient['Рост'] = float(hight)
        button2(message)
    except ValueError:
        bot.send_message(message.from_user.id, 'Введите рост в виде числа')
        bot.register_next_step_handler(message, get_hight2)

def get_weight2(message):
    global new_add_patient
    weight = message.text
    try:
        new_add_patient['Вес'] = float(weight)
        button2(message)
    except ValueError:
        bot.send_message(message.from_user.id, 'Введите вес в виде числа')
        bot.register_next_step_handler(message, get_weight2)

def get_age2(message):
    global new_add_patient
    age = message.text
    try:
        new_add_patient['Возраст'] = int(age)
        button2(message)
    except ValueError:
        bot.send_message(message.from_user.id, 'Введите возраст в виде целого числа')
        bot.register_next_step_handler(message, get_weight2)

def add_sql_patient(new_add_patient):
    global dic
    id_new = max(dic['ID']) + 1
    new_add_patient['ID'] = id_new
    user = list(new_add_patient.items())
    list_user = []
    for i in user:
        if i[1] != None:
            list_user.append(i[1])
        else:
            list_user.append(None)
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO app_patient VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""", tuple(list_user))
    connection.commit()

    connection.close()
    dic = update_data()

def delete_pat(message):
    id = message.text
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    cursor.execute(f"""DELETE FROM app_patient WHERE id = {id}""")
    connection.commit()
    start(message)
    connection.close()
    global dic
    dic = update_data()

bot.polling(none_stop = True)