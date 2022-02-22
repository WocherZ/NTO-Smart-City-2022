import sqlite3
from update_module import *

dic = update_data()

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
        'Рост': 'height'
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