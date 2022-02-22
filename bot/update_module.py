import sql_module

def update_data():
    records = []
    temp_data = sql_module.read_sqlite_table(records)
    dic = {
        'ID': [],
        'Имя': [],
        'Фамилия': [],
        'Логин': [],
        'Пароль': [],
        'Возраст': [],
        'Рост': [],
        'Вес': [],
        'Лечащий доктор': [],
        'Комната': [],
        'Ссылка на фото': [],
        'Диагноз': [],
        'Пол': []
        }

    for j in temp_data:     # в dic все имеющиеся данные у пациентов
        k = 0
        for i in dic:
            dic[i].append(j[k])
            k += 1
    return dic

def update_analysis():
    records = []
    temp_data = sql_module.analisis(records)
    return temp_data